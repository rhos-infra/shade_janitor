from mock import Mock
from unittest import TestCase

from shade_janitor.resources import Resources

class TestBlackList(TestCase):

    def test_blacklist_normal(self):
        r = Resources(Mock())
        instance = Mock()
        instance.name = 'abcde-rdo-ci-88-foo'
        self.assertFalse(r.check_instance_blacklisted(instance))

    def test_blacklist_jenkins(self):
        r = Resources(Mock())
        instance = Mock()
        instance.name = 'jenkins-helper'
        self.assertTrue(r.check_instance_blacklisted(instance))

    def test_blacklist_slave(self):
        r = Resources(Mock())
        instance = Mock()
        instance.name = 'private-slave'
        self.assertTrue(r.check_instance_blacklisted(instance))

    def test_blacklist_slave_2(self):
        r = Resources(Mock())
        instance = Mock()
        instance.name = 'slave-helper'
        self.assertTrue(r.check_instance_blacklisted(instance))

    def test_blacklist_rpm_mirror(self):
        r = Resources(Mock())
        instance = Mock()
        instance.name = 'rpm-mirror-01'
        self.assertTrue(r.check_instance_blacklisted(instance))
