import mock

from shade_janitor import cleanup
from shade_janitor.tests.unit import base


class TestCleanupStack(base.BaseTestCase):

    def setUp(self):
        super(TestCleanupStack, self).setUp()
        self.cloud.delete_stack = mock.Mock()
        self.stack = mock.Mock()

    def add_single(self):
        self.resources._add('stacks', self.stack.id, self.stack.name)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_dry_cleanup_stack(self, mock_stacks_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_stacks_cleanup.called)

    def test_cleanup_stack(self):
        dry_cleanup = False
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(self.cloud.delete_stack.called)

    @mock.patch('shade_janitor.cleanup.show_cleanup')
    def test_cleanup_no_stack(self, mock_stacks_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_stacks_cleanup.called)
        self.assertFalse(self.cloud.delete_stack.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_stacks')
    def test_dry_cleanup_stack_micro(self, mock_stacks_cleanup):
        self.add_single()
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertTrue(mock_stacks_cleanup.called)

    @mock.patch('shade_janitor.cleanup.cleanup_stacks')
    def test_cleanup_stack_micro(self, mock_stacks_cleanup):
        dry_cleanup = False
        self.add_single()
        cleanup.cleanup_resources(
            self.cloud, self.resources.get_selection(), dry_cleanup)
        self.assertTrue(mock_stacks_cleanup.called)

    @mock.patch('shade_janitor.cleanup.dry_cleanup_stacks')
    def test_cleanup_no_stack_micro(self, mock_stacks_cleanup):
        cleanup.cleanup_resources(self.cloud, self.resources.get_selection())
        self.assertFalse(mock_stacks_cleanup.called)
