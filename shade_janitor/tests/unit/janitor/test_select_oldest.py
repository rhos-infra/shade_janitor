from mock import Mock

from shade_janitor.janitor import select_oldest
from shade_janitor.tests.unit import base


class TestSelectOldest(base.BaseTestCase):

    def setUp(self):
        super(TestSelectOldest, self).setUp()
        self.instance = Mock()

    def test_select_oldest_no_old_instances(self):
        select_oldest(self.resources)
        self.assertEqual({}, self.resources._selection)
