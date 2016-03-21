import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupRouterInterface(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupRouterInterface, self).setUp()
        self.cloud.remove_router_interface = mock.Mock()
        self.router = mock.Mock()
        self.router.uuid = 'router-1234'
        self.router2 = mock.Mock()
        self.router2.uuid = 'router-5678'
        self.cloud.search_routers = mock.Mock(return_value=[self.router])

        self.subnet = mock.Mock()
        self.subnet.uuid = '12345'
        self.subnet2 = mock.Mock()
        self.subnet2.uuid = '123456'

    def add_single(self):
        self.resources._add(
            'router_interfaces', self.router.uuid,
            self.router.name, data={'subnet_ids': [self.subnet.uuid]})
        self.resources._add('routers', self.router.uuid, 'router-foo')

    def add_multiple(self):
        self.resources._add(
            'router_interfaces', self.router.uuid,
            self.router.name, data={'subnet_ids': [self.subnet.uuid]})
        self.resources._add('routers', self.router.uuid, 'router-foo')

        self.resources._add(
            'router_interfaces', self.router2.uuid,
            self.router2.name, data={'subnet_ids': [self.subnet2.uuid]})

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_router_interface(self, mock_routers_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_routers_cleanup.called)

    def test_cleanup_router_interface(self):
        dry_cleanup = False
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(self.cloud.remove_router_interface.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_cleanup_no_router_interface(self, mock_routers_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_routers_cleanup.called)
        self.assertFalse(self.cloud.remove_router_interface.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_router_interface_multi(self, mock_routers_cleanup):
        self.add_multiple()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertEqual(3, mock_routers_cleanup.call_count)

    def test_cleanup_router_interface_multi(self):
        self.add_multiple()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)
        self.assertEqual(2, self.cloud.remove_router_interface.call_count)
