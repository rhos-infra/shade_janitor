import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupFloatingIP(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupFloatingIP, self).setUp()
        self.cloud.delete_floating_ip = mock.Mock()
        self.fip = mock.Mock()
        self.fip2 = mock.Mock()

    def add_single_fip(self):
        self.resources._add_floatingip(self.fip)

    def add_double_fip(self):
        self.resources._add_floatingip(self.fip2)
        self.resources._add_floatingip(self.fip)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_floatingIP(self, mock_show_cleanup):
        self.add_single_fip()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_floating_ip.called)
        self.assertTrue(mock_show_cleanup.called)

    def test_cleanup_floatingIP(self):
        self.add_single_fip()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)
        self.assertTrue(self.cloud.delete_floating_ip.called)

    def test_cleanup_no_floatingIP(self):
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)
        self.assertFalse(self.cloud.delete_floating_ip.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_cleanup_no_floatingIP_dry(self, mock_show_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_show_cleanup.called)

    def test_cleanup_floatingIP_multiple(self):
        self.add_double_fip()

        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)

        self.assertEqual(2, self.cloud.delete_floating_ip.call_count)

    def test_cleanup_floatingIP_multiple_dry_run(self):
        self.add_double_fip()

        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=True)

        self.assertFalse(self.cloud.delete_floating_ip.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_floating_ips')
    def test_dry_cleanup_floatingIP_micro(self, mock_floatingIP_cleanup):
        self.resources._add_floatingip(self.fip)
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_floatingIP_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_floating_ips')
    def test_cleanup_floatingIP_micro(self, mock_floatingIP_cleanup):
        dry_cleanup = False
        self.resources._add_floatingip(self.fip)
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_floatingIP_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_floating_ips')
    def test_cleanup_no_floatingIP_micro(self, mock_floatingIP_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_floatingIP_cleanup.called)
