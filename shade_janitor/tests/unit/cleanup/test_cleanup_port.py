import mock
from unittest import TestCase

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupPort(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupPort, self).setUp()
        self.port = mock.Mock()

    @mock.patch('shade_janitor.cleanup.dry_cleanup_ports')
    def test_dry_cleanup_port(self, mock_ports_cleanup):
        self.resources._add('ports', self.port.id,
                            data={'subnet_ids': [],
                                  'network_id': []})
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_ports_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_ports')
    def test_cleanup_port(self, mock_ports_cleanup):
        dry_cleanup=False
        self.resources._add('ports', self.port.id,
                            data={'subnet_ids': [],
                                  'network_id': []})
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_ports_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_ports')
    def test_cleanup_no_port(self, mock_ports_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_ports_cleanup.called)
