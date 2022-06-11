from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add a sample user"""
        User.query.delete()

        user = User(first_name="Salvador", last_name="Gonzalez", image_url="https://randompicturegenerator.com/img/people-generator/g2006a427ed6835a7acfcdcf9dd3ebc97688165cc7da6946d30d9380132e8c0c5467ec9e40e7e28cfb85225c24fe42169_640.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Salvador Gonzalez', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('https://randompicturegenerator.com/img/people-generator/g2006a427ed6835a7acfcdcf9dd3ebc97688165cc7da6946d30d9380132e8c0c5467ec9e40e7e28cfb85225c24fe42169_640.jpg', html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first": "Jerry", "last": "Seinfeld", "image": "https://cdn.britannica.com/70/211670-050-69254076/Jerry-Seinfeld-2019.jpg"}
            resp = client.post("/add-user", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jerry Seinfeld", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/{self.user_id}/delete-user", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("All Users", html)
            self.assertNotIn("Salvador Gonzalez", html)