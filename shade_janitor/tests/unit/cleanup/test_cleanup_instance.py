import mock
from unittest import TestCase

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupInstance(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupInstance, self).setUp()
        self.instance = mock.Mock()

    @mock.patch('shade_janitor.cleanup.dry_cleanup_instances')
    def test_dry_cleanup_instance(self, mock_instances_cleanup):
        self.resources._add_instance(self.instance)
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_instances_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_instances')
    def test_cleanup_instance(self, mock_instances_cleanup):
        dry_cleanup=False
        self.resources._add_instance(self.instance)
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_instances_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_instances')
    def test_cleanup_no_instance(self, mock_instances_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_instances_cleanup.called)
