import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupPort(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupPort, self).setUp()
        self.cloud.delete_port = mock.Mock()
        self.port = mock.Mock()
        self.port.uuid = '1234'
        self.port2 = mock.Mock()
        self.port2.uuid = '5678'

    def add_single(self):
        self.resources._add('ports', self.port.uuid)

    def add_multiple(self):
        self.resources._add('ports', self.port.uuid)
        self.resources._add('ports', self.port2.uuid)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_port(self, mock_ports_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_ports_cleanup.called)

    def test_cleanup_port(self):
        self.add_single()
        mock_ports_cleanup = self.cloud.delete_port
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)
        self.assertTrue(mock_ports_cleanup.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_cleanup_no_port_dry(self, mock_ports_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_ports_cleanup.called)

    def test_cleanup_no_port(self):
        mock_ports_cleanup = self.cloud.delete_port
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_ports_cleanup.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_port_multiple(self, mock_ports_cleanup):
        self.add_multiple()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertEqual(2, mock_ports_cleanup.call_count)

    def test_cleanup_port_multiple(self):
        self.add_multiple()
        mock_ports_cleanup = self.cloud.delete_port
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_run=False)
        self.assertEqual(2, mock_ports_cleanup.call_count)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_ports')
    def test_dry_cleanup_port_micro(self, mock_ports_cleanup):
        self.resources._add('ports', self.port.id,
                            data={'subnet_ids': [],
                                  'network_id': []})
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_ports_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_ports')
    def test_cleanup_port_micro(self, mock_ports_cleanup):
        dry_cleanup = False
        self.resources._add('ports', self.port.id,
                            data={'subnet_ids': [],
                                  'network_id': []})
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_ports_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_ports')
    def test_cleanup_no_port_micro(self, mock_ports_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_ports_cleanup.called)
