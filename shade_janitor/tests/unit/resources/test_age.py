import datetime
import mock
from pytz import utc
from shade_janitor.tests.unit import base

from shade_janitor.select_age import SelectAgeRelatedResources


class FakeInstance(dict):
    NOW = datetime.datetime(2000, 1, 10, 0, 0, 1, tzinfo=utc)

    def __init__(self, name, created_ago, power_state=1):
        super(FakeInstance, self).__init__()

        self.id = name
        self.name = name
        # we force to be 1 second before requested time
        # (due to condition being 'greater-then', but not equal)
        self.created = str(
            self.NOW - created_ago - datetime.timedelta(seconds=1)
        )
        self['OS-EXT-STS:power_state'] = power_state


class TestSelectAge(base.BaseTestCase):

    def setUp(self):
        super(TestSelectAge, self).setUp()
        self.maxDiff = None

        self._td_0 = datetime.timedelta(hours=0)
        self._td_1h = datetime.timedelta(hours=1)
        self._td_2h = datetime.timedelta(hours=2)
        self._td_4h = datetime.timedelta(hours=4)
        self._td_2d = datetime.timedelta(days=2)
        self._td_30d = datetime.timedelta(days=30)
        self._young = {'instances': {
            '1H_Off': FakeInstance('1H_Off', self._td_1h, 0),
            '2H_Active': FakeInstance('2H_Active', self._td_2h),
            'young_permanent': FakeInstance('young_permanent', self._td_1h),
        }}
        self._old = {'instances': {
            '30D_Off': FakeInstance('30D_Off', self._td_30d, 0),
            '2H_Off': FakeInstance('2H_Off', self._td_2h, 0),
            '4H_Active': FakeInstance('4H_Active', self._td_4h),
            'old_permanent': FakeInstance('old_permanent', self._td_2d),
        }}
        self._all_as_list = (self._old['instances'].values() +
                             self._young['instances'].values())

    def test_select_age_no_instances(self):
        """Nothing selected when there are no servers"""
        cloud = mock.Mock()
        cloud.list_servers = mock.Mock(return_value=[])
        resources = SelectAgeRelatedResources(cloud)
        resources.select_old_instances()
        self.assertEqual({}, resources.get_selection())

    def test_select_age_old(self):
        """Select older instances"""
        cloud = mock.Mock()
        cloud.list_servers = mock.Mock(
            return_value=self._old['instances'].values())

        resources = SelectAgeRelatedResources(cloud)
        resources.select_old_instances(powered_off_ttl=self._td_2h,
                                       powered_on_ttl=self._td_4h,
                                       powered_on_permanent_ttl=self._td_2d,
                                       now=FakeInstance.NOW
                                       )

        self.assertTrue(resources.is_permanent(
            self._old['instances']['old_permanent']))
        self.assertEqual(self._old['instances'].keys(),
                         resources.get_selection()['instances'].keys())

    def test_select_age_no_young(self):
        """Do not select young(er) instances"""
        cloud = mock.Mock()
        cloud.list_servers = mock.Mock(
            return_value=self._young['instances'].values())

        resources = SelectAgeRelatedResources(cloud)
        resources.select_old_instances(powered_off_ttl=self._td_2h,
                                       powered_on_ttl=self._td_4h,
                                       powered_on_permanent_ttl=self._td_2d,
                                       now=FakeInstance.NOW
                                       )

        self.assertTrue(resources.is_permanent(
            self._young['instances']['young_permanent']))
        self.assertEqual({}, resources.get_selection())

    def test_select_noage(self):
        """Zero ttl means do not selected, even when very old"""
        cloud = mock.Mock()
        cloud.list_servers = mock.Mock(return_value=self._all_as_list)
        resources = SelectAgeRelatedResources(cloud)
        resources.select_old_instances(powered_off_ttl=self._td_0,
                                       powered_on_ttl=self._td_0,
                                       powered_on_permanent_ttl=self._td_0
                                       )
        self.assertEqual({}, resources.get_selection())
