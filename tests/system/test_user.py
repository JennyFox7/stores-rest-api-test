from models.user import UserModel
from tests.base_test import BaseTest
import json

# testing the registration and authorization of users

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                response = client.post("/register", json={"username": "test user", "password": "1234"})

                self.assertIsNotNone(UserModel.find_by_id(1),
                                     "No user is existing but shall be.")
                self.assertIsNotNone(UserModel.find_by_username('test user'),
                                     "The 'test user' is not existing but shall be.")
                self.assertEqual(response.status_code, 201,
                                 "No user could be created.")
                self.assertDictEqual({'message': 'User created successfully.'}, json.loads(response.data),
                                     "The success message is not sent but shall be.")


    def test_register_and_login(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                client.post("/register", json={"username": "test user", "password": "1234"})
                auth_response = client.post('/auth',
                                           data=json.dumps({"username": "test user", "password": "1234"}),
                                           headers={'Content-Type': 'application/json'})
                # auth response returns dict with access_token {'access_token': 'ahjashdhfohfiwewovw'}

                self.assertIn('access_token', json.loads(auth_response.data).keys())  # transfers auth.data into json and takes the keys access_token
                # this token has to be sent to endpoint to login

    def test_register_duplicate_user(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                # first request registers the user first
                client.post("/register", json={"username": "test user", "password": "1234"})
                # second response does the same
                response = client.post("/register", json={"username": "test user", "password": "1234"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data), {"message": "A user with that username already exists"})

