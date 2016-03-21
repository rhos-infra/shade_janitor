import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupInstance(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupInstance, self).setUp()
        self.cloud.delete_server = mock.Mock()
        self.instance = mock.Mock()

    def add_single(self):
        self.resources._add_instance(self.instance)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_instance(self, mock_show_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_server.called)
        self.assertTrue(mock_show_cleanup.called)

    def test_cleanup_instance(self):
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)
        self.assertTrue(self.cloud.delete_server.called)

    def test_cleanup_no_instance(self):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_server.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_no_instance(self, mock_show_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_server.called)
