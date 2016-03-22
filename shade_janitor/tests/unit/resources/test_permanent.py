from mock import Mock

from shade_janitor.tests.unit import base


class TestPermanentResources(base.BaseTestCase):

    def setUp(self):
        super(TestPermanentResources, self).setUp()
        self.instance = Mock()

    def test_is_permanent_non_perm_instance(self):
        self.instance.name = 'abcde-rdo-ci-88-foo'
        self.assertFalse(self.resources.is_permanent(self.instance))

    def test_is_permanent_perm_instance(self):
        self.instance.name = 'permanent-rdo-ci-88-foo'
        self.assertTrue(self.resources.is_permanent(self.instance))

    def test_name_empty(self):
        self.instance.name = ''
        self.assertFalse(self.resources.is_permanent(self.instance))

    def test_name_none(self):
        self.instance.name = None
        self.assertFalse(self.resources.is_permanent(self.instance))

    def test_none(self):
        self.assertFalse(self.resources.is_permanent(None))
