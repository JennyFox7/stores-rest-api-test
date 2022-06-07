"""
This base test imports the app (including StoreModel) for all unit tests
so that the "unused" import line will not be shown on each unit test
"""

from app import app
from unittest import TestCase

class UnitBaseTest(TestCase):
    pass