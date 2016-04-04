import mock
from shade_janitor.tests.unit import base

from shade_janitor.select_age import SelectAgeRelatedResources


class TestSelectAge(base.BaseTestCase):

    def setUp(self):
        super(TestSelectAge, self).setUp()

    def test_select_age_no_instances(self):
        cloud = mock.Mock()
        cloud.list_servers = mock.Mock(return_value=[])
        resources = SelectAgeRelatedResources(cloud)
        resources.select_old_instances()
        self.assertEqual({}, resources.get_selection())
