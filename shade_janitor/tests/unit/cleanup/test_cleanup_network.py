import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupNetwork(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupNetwork, self).setUp()
        self.cloud.delete_network = mock.Mock()
        self.network = mock.Mock()

    def add_single(self):
        self.resources._add('nets', self.network.id, self.network.name)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_network(self, mock_show_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_show_cleanup.called)

    def test_cleanup_network(self):
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)
        self.assertTrue(self.cloud.delete_network.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_cleanup_no_network(self, mock_show_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_show_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_networks')
    def test_dry_cleanup_network_micro(self, mock_networks_cleanup):
        self.resources._add('nets', self.network.id, self.network.name)
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_networks_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_networks')
    def test_cleanup_network_micro(self, mock_networks_cleanup):
        dry_cleanup = False
        self.resources._add('nets', self.network.id, self.network.name)
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_networks_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_networks')
    def test_cleanup_no_network_micro(self, mock_networks_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_networks_cleanup.called)
