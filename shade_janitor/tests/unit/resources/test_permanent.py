from mock import Mock
from unittest import TestCase

from shade_janitor.resources import Resources


class TestPermanentResources(TestCase):

    def test_is_permanent_non_perm_instance(self):
        r = Resources(Mock())
        instance = Mock()
        instance.name = 'abcde-rdo-ci-88-foo'
        self.assertFalse(r.is_permanent(instance))

    def test_is_permanent_perm_instance(self):
        r = Resources(Mock())
        instance = Mock()
        instance.name = 'permanent-rdo-ci-88-foo'
        self.assertTrue(r.is_permanent(instance))
