import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupSecurityGroup(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupSecurityGroup, self).setUp()
        self.cloud.delete_security_group = mock.Mock()
        self.secgroup = mock.Mock()

    def add_single(self):
        self.resources._add('secgroups', '1', 'foobar_secgroup')

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_secgroup(self, mock_show_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_security_group.called)
        self.assertTrue(mock_show_cleanup.called)

    def test_cleanup_secgroup(self):
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)
        self.assertTrue(self.cloud.delete_security_group.called)

    def test_cleanup_no_secgroup(self):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_security_group.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_no_secgroup(self, mock_show_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_security_group.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_secgroups')
    def test_dry_cleanup_secgroup_micro(self, mock_secgroups_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_secgroups_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_secgroups')
    def test_cleanup_secgroup_micro(self, mock_secgroups_cleanup):
        dry_cleanup = False
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_secgroups_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_secgroups')
    def test_cleanup_no_secgroup_micro(self, mock_secgroups_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_secgroups_cleanup.called)
