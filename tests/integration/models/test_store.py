from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest

class StoreTest(BaseTest):
    def test_inital_item(self):
        store = StoreModel('test store')

        self.assertListEqual(store.items.all(), [], "The store lists items but no items were added.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test store')

            self.assertIsNone(StoreModel.find_by_name('test store'), "The 'test store' is already existing but shall not.")

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test store'), "The 'test store' is not exiting but shall be.")

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test store'), "The 'test store' is still existing but shall not.")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test store')
            item = ItemModel('test item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test item')

    def test_store_json(self):
        store = StoreModel('test store')
        expected = {
            'name': 'test store',
            'items': []
        }

        self.assertDictEqual(store.json(), expected, "The 'test store' is not initialized correctly.")

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test store')
            item = ItemModel('test item', 19.99, 1)
            expected = {
                'name': 'test store',
                'items': [{
                    'name': 'test item',
                    'price': 19.99
                }]
            }

            store.save_to_db()
            item.save_to_db()

            self.assertDictEqual(store.json(), expected, "The 'test store' does not contain the 'test item' in an items list.")
