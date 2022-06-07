from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test user', 'test password')

        self.assertEqual(user.username, 'test user', "Name of user is not as expected.")
        self.assertEqual(user.password, 'test password', "Password of user is not as expected.")