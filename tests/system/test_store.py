from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

# testing the creation, finding and deletion of stores with items

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                response = client.post('/store/test_store')

                self.assertIsNotNone(StoreModel.find_by_name("test_store"),
                                     "No test_store is existing but shall be.")
                self.assertEqual(response.status_code, 201,
                                 "No store could be created.")
                self.assertDictEqual({
                    'id': 1,
                    'name': 'test_store',
                    'items': []},
                    json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                client.post('/store/test_store')
                response = client.post('/store/test_store')

                self.assertEqual(response.status_code, 400,
                                 "Request got through but shall not.")
                self.assertEqual(json.loads(response.data),
                                 {'message': "A store with name 'test_store' already exists."},
                                 "Duplicate of store was created but shall not.")

    def test_delete_store(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                client.post('/store/test_store')
                response = client.delete('/store/test_store')

                self.assertIsNone(StoreModel.find_by_name("test_store"),
                                     "The test_store is still existing but shall not.")
                self.assertDictEqual(json.loads(response.data),
                                 {'message': 'Store deleted'},
                                 "Store was not deleted.")

    def test_find_store(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                client.post('/store/test_store')
                response = client.get('/store/test_store')

                self.assertEqual(response.status_code, 200,
                                  "The status code does not return 200 but shall do.")
                self.assertIsNotNone(json.loads(response.data),
                                 "Store was not found.")

    def test_store_not_found(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                response = client.get('/store/test_store')

                self.assertEqual(response.status_code, 404,
                                    "The status code was not 404 as expected.")
                self.assertDictEqual(json.loads(response.data),
                                 {'message': 'Store not found'},
                                 "Store was found but shall not exist.")

    def test_store_found_with_items(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                StoreModel('test_store').save_to_db() # same as: response = client.get('/store/test_store')
                ItemModel('test_item', 19.99, 1).save_to_db()
                response = client.get('/store/test_store')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'test_store', 'items': [{'name': 'test_item', 'price': 19.99}]},
                                     json.loads(response.data))


    def test_store_list(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                StoreModel('test_store').save_to_db()
                response = client.get('/stores')

                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test_store', 'items': []}]}, json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:  # get client to interact with app
            with self.app_context():  # initialize database and retrieve data from it
                StoreModel('test_store').save_to_db()  # same as: response = client.get('/store/test_store')
                ItemModel('test_item', 19.99, 1).save_to_db()
                response = client.get('/stores')

                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test_store', 'items': [{'name': 'test_item', 'price': 19.99}]}]},
                                     json.loads(response.data))

