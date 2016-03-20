import mock
from unittest import TestCase

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupFloatingIP(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupFloatingIP, self).setUp()
        self.fip = mock.Mock()

    @mock.patch('shade_janitor.cleanup.dry_cleanup_floating_ips')
    def test_dry_cleanup_floatingIP(self, mock_floatingIP_cleanup):
        self.resources._add_floatingip(self.fip)
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_floatingIP_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_floating_ips')
    def test_cleanup_floatingIP(self, mock_floatingIP_cleanup):
        dry_cleanup=False
        self.resources._add_floatingip(self.fip)
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_floatingIP_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_floating_ips')
    def test_cleanup_no_floatingIP(self, mock_floatingIP_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_floatingIP_cleanup.called)
