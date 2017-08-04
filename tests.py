import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """ Test to see if homepage displays. """

        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        """ A test to show we see the RSVP form, but NOT the party details. """

        result = self.client.get("/")
        self.assertIn("<h2>Please RSVP</h2>", result.data)
        self.assertNotIn("123 Magic Unicorn Way", result.data)

    def test_rsvp(self):
        """ See if user sees party details but not RSVP form. """

        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)

        result = self.client.get("/")
        self.assertIn("123 Magic Unicorn Way", result.data)  # check address
        self.assertNotIn("<h2>Please RSVP</h2>", result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        """ Test that the games page displays the game from example_data(). """

        result = self.client.get("/games")
        self.assertIn("ticket_to_ride2", result.data)

if __name__ == "__main__":
    unittest.main()
