import datetime
import mock
from pytz import utc
from unittest import TestCase

from shade_janitor.resources import Resources


class FakeInstance(dict):
    NOW = datetime.datetime(2000, 1, 10, 0, 0, 1, tzinfo=utc)

    def __init__(self, name, created_ago, status='ACTIVE'):
        super(FakeInstance, self).__init__()

        self.id = name
        self.name = name
        # we force to be 1 second before requested time
        # (due to condition being 'greater-then', but not equal)
        self.created = str(
            self.NOW - created_ago - datetime.timedelta(seconds=1)
        )
        self.status = status
        self['OS-EXT-STS:power_state'] = 0 if status == 'SHUTOFF' else 1


class BaseTestCase(TestCase):

    def setUp(self):
        self.cloud = mock.Mock()
        self.resources = Resources(self.cloud)
        self._td_0 = datetime.timedelta(hours=0)
        self._td_1h = datetime.timedelta(hours=1)
        self._td_2h = datetime.timedelta(hours=2)
        self._td_4h = datetime.timedelta(hours=4)
        self._td_2d = datetime.timedelta(days=2)
        self._td_30d = datetime.timedelta(days=30)

        self._young = {'instances': {
            '1H_Off': FakeInstance('1H_Off', self._td_1h, 'SHUTOFF'),
            '2H_Active': FakeInstance('2H_Active', self._td_2h),
            '0H_Error': FakeInstance('1H_Error', self._td_0, 'ERROR'),
            'young_permanent': FakeInstance('young_permanent', self._td_1h),
        }}
        self._old = {'instances': {
            '30D_Off': FakeInstance('30D_Off', self._td_30d, 'SHUTOFF'),
            '2H_Off': FakeInstance('2H_Off', self._td_2h, 'SHUTOFF'),
            '4H_Active': FakeInstance('4H_Active', self._td_4h),
            '2H_Error': FakeInstance('2H_Error', self._td_2h, 'ERROR'),
            'old_permanent': FakeInstance('old_permanent', self._td_2d),
        }}
        self._all_as_list = (self._old['instances'].values() +
                             self._young['instances'].values())

    def getCloudNoInstances(self):
        cloud = mock.Mock()
        cloud.list_servers = mock.Mock(return_value=[])
        return cloud

    def getCloudYoungInstance(self):
        cloud = mock.Mock()
        cloud.list_servers = mock.Mock(
            return_value=self._young['instances'].values())
        cloud.list_networks = mock.Mock(return_value=[])
        cloud.list_subnets = mock.Mock(return_value=[])
        cloud.list_routers = mock.Mock(return_value=[])
        cloud.list_ports = mock.Mock(return_value=[])
        cloud.list_floating_ips = mock.Mock(return_value=[])
        cloud.list_stacks = mock.Mock(return_value=[])
        cloud.list_keypairs = mock.Mock(return_value=[])
        cloud.list_security_groups = mock.Mock(return_value=[])
        return cloud

    def getCloudOldInstance(self):
        cloud = mock.Mock()
        cloud.list_servers = mock.Mock(
            return_value=self._old['instances'].values())
        cloud.list_networks = mock.Mock(return_value=[])
        cloud.list_subnets = mock.Mock(return_value=[])
        cloud.list_routers = mock.Mock(return_value=[])
        cloud.list_ports = mock.Mock(return_value=[])
        cloud.list_floating_ips = mock.Mock(return_value=[])
        cloud.list_stacks = mock.Mock(return_value=[])
        cloud.list_keypairs = mock.Mock(return_value=[])
        cloud.list_security_groups = mock.Mock(return_value=[])
        return cloud

    def getCloudYoungAndOldInstances(self):
        cloud = mock.Mock()
        cloud.list_servers = mock.Mock(return_value=self._all_as_list)
        cloud.list_networks = mock.Mock(return_value=[])
        cloud.list_subnets = mock.Mock(return_value=[])
        cloud.list_routers = mock.Mock(return_value=[])
        cloud.list_ports = mock.Mock(return_value=[])
        cloud.list_floating_ips = mock.Mock(return_value=[])
        cloud.list_stacks = mock.Mock(return_value=[])
        cloud.list_keypairs = mock.Mock(return_value=[])
        cloud.list_security_groups = mock.Mock(return_value=[])
        return cloud
