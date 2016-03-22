import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupRouter(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupRouter, self).setUp()
        self.cloud.delete_router = mock.Mock()
        self.router = mock.Mock()

    def add_single(self):
        self.resources._add('routers', self.router.id, self.router.name)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_router(self, mock_routers_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_routers_cleanup.called)

    def test_cleanup_router(self):
        dry_cleanup = False
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(self.cloud.delete_router.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_cleanup_no_router(self, mock_routers_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_routers_cleanup.called)
        self.assertFalse(self.cloud.delete_router.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_routers')
    def test_dry_cleanup_router_micro(self, mock_routers_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_routers_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_routers')
    def test_cleanup_router_micro(self, mock_routers_cleanup):
        dry_cleanup = False
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_routers_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_routers')
    def test_cleanup_no_router_micro(self, mock_routers_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_routers_cleanup.called)
