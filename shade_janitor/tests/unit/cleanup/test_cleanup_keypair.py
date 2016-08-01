import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupKeypair(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupKeypair, self).setUp()
        self.cloud.delete_keypair = mock.Mock()
        self.keypair = mock.Mock()

    def add_single(self):
        self.resources._add('keypairs', '1', 'foobar_keypair')

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_keypair(self, mock_show_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_keypair.called)
        self.assertTrue(mock_show_cleanup.called)

    def test_cleanup_keypair(self):
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)
        self.assertTrue(self.cloud.delete_keypair.called)

    def test_cleanup_no_keypair(self):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_keypair.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_no_keypair(self, mock_show_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(self.cloud.delete_keypair.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_keypairs')
    def test_dry_cleanup_keypair_micro(self, mock_keypairs_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_keypairs_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_keypairs')
    def test_cleanup_keypair_micro(self, mock_keypairs_cleanup):
        dry_cleanup = False
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_keypairs_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_keypairs')
    def test_cleanup_no_keypair_micro(self, mock_keypairs_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_keypairs_cleanup.called)
