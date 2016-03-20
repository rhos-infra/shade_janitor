import mock
from unittest import TestCase

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupNetwork(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupNetwork, self).setUp()
        self.network = mock.Mock()

    @mock.patch('shade_janitor.cleanup.dry_cleanup_networks')
    def test_dry_cleanup_network(self, mock_networks_cleanup):
        self.resources._add('nets', self.network.id, self.network.name)
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_networks_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_networks')
    def test_cleanup_network(self, mock_networks_cleanup):
        dry_cleanup=False
        self.resources._add('nets', self.network.id, self.network.name)
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_networks_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_networks')
    def test_cleanup_no_network(self, mock_networks_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_networks_cleanup.called)
