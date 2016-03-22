import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupSubnet(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupSubnet, self).setUp()
        self.cloud.delete_subnet = mock.Mock()
        self.subnet = mock.Mock()

    def add_single(self):
        self.resources._add('subnets', self.subnet.id, self.subnet.name)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_subnet(self, mock_subnets_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_subnets_cleanup.called)

    def test_cleanup_subnet(self):
        dry_cleanup = False
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(self.cloud.delete_subnet.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_cleanup_no_subnet(self, mock_subnets_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_subnets_cleanup.called)
        self.assertFalse(self.cloud.delete_subnet.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_subnets')
    def test_dry_cleanup_subnet_micro(self, mock_subnets_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_subnets_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_subnets')
    def test_cleanup_subnet_micro(self, mock_subnets_cleanup):
        dry_cleanup = False
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_subnets_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_subnets')
    def test_cleanup_no_subnet_micro(self, mock_subnets_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_subnets_cleanup.called)
