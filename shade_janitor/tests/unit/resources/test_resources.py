from mock import Mock

from shade_janitor.tests.unit import base


class TestResources(base.BaseTestCase):

    def setUp(self):
        super(TestResources, self).setUp()
        self.instance = Mock()

        self._mock_instance = Mock()
        self._mock_instance.id = '12345-6789'
        self._mock_instance.name = '12345-instance'
        self._mock_instance.created = 'foo-date'

    def test_no_add_no_instances(self):
        self.assertNotIn('instances', self.resources._selection)

    def test_add_none_instances(self):
        self.resources._add_instance(None)
        self.assertNotIn('instances', self.resources._selection)

    def test_add_instance_simple(self):
        self.resources._add_instance(self._mock_instance)
        self.assertIn('instances', self.resources._selection)
        self.assertEqual(1, len(self.resources._selection['instances']))

    def test_add_instance_age_string(self):
        self.resources._add_instance(self._mock_instance, age='05:00:00')
        self.assertIn('instances', self.resources._selection)
        self.assertEqual(1, len(self.resources._selection['instances']))

    def test_add_instance_age_number(self):
        self.resources._add_instance(self._mock_instance, age=5)
        self.assertIn('instances', self.resources._selection)
        self.assertEqual(1, len(self.resources._selection['instances']))

    def test_add_resource_none_uuid_name(self):
        self.resources._add('foo', None, None)
        self.assertNotIn('foo', self.resources._selection)

    def test_add_resource_uuid_none_name(self):
        self.resources._add('foo', 'uuid1', None)
        self.assertIn('foo', self.resources._selection)
        self.assertIn('uuid1', self.resources._selection['foo'])
        self.assertEqual(1, len(self.resources._selection['foo']))

    def test_add_resource_uuid_name(self):
        self.resources._add('foo', 'uuid1', 'name1')
        self.assertIn('foo', self.resources._selection)
        self.assertIn('uuid1', self.resources._selection['foo'])
        self.assertEqual(1, len(self.resources._selection['foo']))

    def test_reset_nothing(self):
        self.resources.reset()
        self.assertEqual(0, len(self.resources._selection))

    def test_add_reset(self):
        self.resources._add('foo', 'uuid1', 'name1')
        self.resources.reset()
        self.assertNotIn('foo', self.resources._selection)

    def test_add_reset_add(self):
        self.resources._add('foo', 'uuid1', 'name1')
        self.resources.reset()
        self.resources._add('foo', 'uuid2', 'name2')
        self.assertIn('foo', self.resources._selection)
        self.assertIn('uuid2', self.resources._selection['foo'])
        self.assertEqual(1, len(self.resources._selection['foo']))
