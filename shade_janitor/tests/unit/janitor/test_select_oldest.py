import mock

from shade_janitor.janitor import select_oldest
from shade_janitor.tests.unit import base_age_related


class TestSelectOldest(base_age_related.BaseTestCase):

    def setUp(self):
        super(TestSelectOldest, self).setUp()
        self.args = mock.Mock()
        self.args.old_active = 8
        self.args.old_inactive = 1
        self.args.old_permanent = 14
        self.args.old_inerrror = 1

    def test_cloud_None(self):
        self.assertEqual(None, select_oldest(None, None))

    def test_cloud_mock_no_args(self):
        cloud = self.getCloudNoInstances()
        self.assertEqual(None, select_oldest(cloud, None))

    def test_cloud_mock_gives_resources_selection_back(self):
        cloud = self.getCloudNoInstances()
        self.assertNotEqual(None, select_oldest(cloud, self.args))

    def test_no_old_instances_none_selected(self):
        cloud = self.getCloudNoInstances()
        resources = select_oldest(cloud, self.args)
        self.assertEqual({}, resources._selection)

    def test_select_oldest_one_new_instances(self):
        cloud = self.getCloudOldInstance()
        resources = select_oldest(cloud, self.args)
        self.assertIn('instances', resources._selection)
