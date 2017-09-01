from mock import Mock

from shade_janitor.tests.unit import base


class TestBlackList(base.BaseTestCase):

    def setUp(self):
        super(TestBlackList, self).setUp()
        self.instance = Mock()

    def test_blacklist_normal(self):
        self.instance.name = 'abcde-rdo-ci-88-foo'
        self.assertFalse(self.resources.is_blacklisted(self.instance))

    def test_blacklist_jenkins(self):
        self.instance.name = 'jenkins-helper'
        self.assertTrue(self.resources.is_blacklisted(self.instance))

    def test_blacklist_slave(self):
        self.instance.name = 'private-slave'
        self.assertTrue(self.resources.is_blacklisted(self.instance))

    def test_blacklist_slave_2(self):
        self.instance.name = 'slave-helper'
        self.assertTrue(self.resources.is_blacklisted(self.instance))

    def test_blacklist_rpm_mirror(self):
        self.instance.name = 'rpm-mirror-01'
        self.assertTrue(self.resources.is_blacklisted(self.instance))

    def test_empty(self):
        self.instance.name = ''
        self.assertFalse(self.resources.is_blacklisted(self.instance))

    def test_name_none(self):
        self.instance.name = None
        self.assertFalse(self.resources.is_blacklisted(self.instance))

    def test_none(self):
        self.assertFalse(self.resources.is_blacklisted(None))

    def test_custom_blacklist(self):
        self.resources.blacklist.append("mario")
        self.instance.name = "its-a-me-mario"
        self.assertTrue(self.resources.is_blacklisted(self.instance))
