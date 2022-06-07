from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):  # setting up the authorization
        super(ItemTest, self).setUp() # calling the setUp method from BaseTest
        with self.app() as client:
            with self.app_context():
                UserModel('test user', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data = json.dumps({'username': 'test user', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'  # convention from flask jwt

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')

                self.assertEqual(response.status_code, 401)  # because there was no auth header, 401 means "you are not logged in"

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test item', 19.99, 1).save_to_db()
                response = client.get('/item/test item', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 200,
                                    "The status code does not return 200 but shall do.")
                self.assertIsNotNone(json.loads(response.data),
                                     "Item was not found.")

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test item', 19.99, 1).save_to_db()
                response = client.delete('/item/test item')  # auth header is only needed for "get" requests

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'Item deleted'},
                                     "Item was not deleted.")

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                response = client.post('/item/test item', json={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201, "Status code is expected to be 201.")
                self.assertDictEqual(json.loads(response.data), {'name': 'test item', 'price': 19.99})

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test item', 19.99, 1).save_to_db()
                response = client.post('/item/test item', json={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 400, "Status code is expected to be 400.")
                self.assertDictEqual(json.loads(response.data), {'message': "An item with name 'test item' already exists."})

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                response = client.put('/item/test item', json={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200, "Status code is expected to be 201.")
                self.assertEqual(ItemModel.find_by_name('test item').price, 19.99)
                self.assertDictEqual(json.loads(response.data), {'name': 'test item', 'price': 19.99})

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test item', 19.99, 1).save_to_db()
                response = client.put('/item/test item', json={'price': 17.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200, "Status code is expected to be 201.")
                self.assertEqual(ItemModel.find_by_name('test item').price, 17.99)
                self.assertDictEqual(json.loads(response.data), {'name': 'test item', 'price': 17.99})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()

                ItemModel('test item', 19.99, 1).save_to_db()
                response = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test item', 'price': 19.99}]}, json.loads(response.data))

