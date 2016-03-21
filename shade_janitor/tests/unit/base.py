import mock
from unittest import TestCase

from shade_janitor.resources import Resources


class BaseTestCase(TestCase):

    def setUp(self):
        self.cloud = mock.Mock()
        self.resources = Resources(mock.Mock())
