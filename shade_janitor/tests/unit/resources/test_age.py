from shade_janitor.select_age import SelectAgeRelatedResources
from shade_janitor.tests.unit import base_age_related
from shade_janitor.tests.unit.base_age_related import FakeInstance


class TestSelectAge(base_age_related.BaseTestCase):

    def setUp(self):
        super(TestSelectAge, self).setUp()
        pass

    def test_select_age_no_instances(self):
        """Nothing selected when there are no servers"""
        cloud = self.getCloudNoInstances()

        resources = SelectAgeRelatedResources(cloud)
        resources.select_old_instances()
        self.assertEqual({}, resources.get_selection())

    def test_select_age_old(self):
        """Select older instances"""
        cloud = self.getCloudOldInstance()

        resources = SelectAgeRelatedResources(cloud)
        resources.select_old_instances(powered_off_ttl=self._td_2h,
                                       powered_on_ttl=self._td_4h,
                                       powered_on_permanent_ttl=self._td_2d,
                                       inerror_ttl=self._td_1h,
                                       now=FakeInstance.NOW
                                       )

        self.assertTrue(resources.is_permanent(
            self._old['instances']['old_permanent']))
        self.assertEqual(self._old['instances'].keys(),
                         resources.get_selection()['instances'].keys())

    def test_select_age_no_young(self):
        """Do not select young(er) instances"""
        cloud = self.getCloudYoungInstance()

        resources = SelectAgeRelatedResources(cloud)
        resources.select_old_instances(powered_off_ttl=self._td_2h,
                                       powered_on_ttl=self._td_4h,
                                       powered_on_permanent_ttl=self._td_2d,
                                       inerror_ttl=self._td_1h,
                                       now=FakeInstance.NOW
                                       )

        self.assertTrue(resources.is_permanent(
            self._young['instances']['young_permanent']))
        self.assertEqual({}, resources.get_selection())

    def test_select_noage(self):
        """Zero ttl means do not selected, even when very old"""
        cloud = self.getCloudYoungAndOldInstances()

        resources = SelectAgeRelatedResources(cloud)
        resources.select_old_instances(powered_off_ttl=self._td_0,
                                       powered_on_ttl=self._td_0,
                                       powered_on_permanent_ttl=self._td_0
                                       )
        self.assertEqual({}, resources.get_selection())
