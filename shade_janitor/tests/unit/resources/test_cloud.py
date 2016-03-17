<<<<<<< HEAD
from mock import Mock
=======
>>>>>>> upstream/master
from unittest import TestCase

from shade_janitor.resources import NoCloudException
from shade_janitor.resources import Resources

<<<<<<< HEAD
=======

>>>>>>> upstream/master
class TestResourcesCloud(TestCase):

    def test_resources_fails_no_cloud(self):
        with self.assertRaises(NoCloudException):
            Resources(None)
