import unittest
from shade_janitor.resources import SelectRelatedResources
from mock import Mock


class TestResources(unittest.TestCase):

    def test_resources_fails_no_cloud(self):
        with self.assertRaises(Exception):
            SelectRelatedResources(None)

    def test_blacklist_normal(self):
        r = SelectRelatedResources(Mock())
        instance = Mock()
        instance.name = 'abcde-rdo-ci-88-foo'
        self.assertFalse(r.check_instance_blacklisted(instance))

    def test_blacklist_jenkins(self):
        r = SelectRelatedResources(Mock())
        instance = Mock()
        instance.name = 'jenkins-helper'
        self.assertTrue(r.check_instance_blacklisted(instance))

    def test_blacklist_slave(self):
        r = SelectRelatedResources(Mock())
        instance = Mock()
        instance.name = 'private-slave'
        self.assertTrue(r.check_instance_blacklisted(instance))

    def test_blacklist_slave_2(self):
        r = SelectRelatedResources(Mock())
        instance = Mock()
        instance.name = 'slave-helper'
        self.assertTrue(r.check_instance_blacklisted(instance))

    def test_blacklist_rpm_mirror(self):
        r = SelectRelatedResources(Mock())
        instance = Mock()
        instance.name = 'rpm-mirror-01'
        self.assertTrue(r.check_instance_blacklisted(instance))

    def test_is_permanent_non_perm_instance(self):
        r = SelectRelatedResources(Mock())
        instance = Mock()
        instance.name = 'abcde-rdo-ci-88-foo'
        self.assertFalse(r.check_instance_permenant(instance))

    def test_is_permanent_perm_instance(self):
        r = SelectRelatedResources(Mock())
        instance = Mock()
        instance.name = 'permanent-rdo-ci-88-foo'
        self.assertTrue(r.check_instance_permenant(instance))
