import mock
from unittest import TestCase

from shade_janitor.resources import NoCloudException
from shade_janitor.resources import Resources


class TestResourcesCloud(TestCase):

    def test_resources_fails_no_cloud(self):
        with self.assertRaises(NoCloudException):
            Resources(None)

    def test_passes_with_something(self):
        Resources(mock.Mock())
