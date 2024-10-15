"""tests/unit/task_test.py"""

import unittest
from datetime import datetime
from unittest.mock import patch

from protaskinate.entities.task import Task, TaskPriority, TaskStatus
from protaskinate.services.task_service import TaskService


class TestTask(unittest.TestCase):
    """Test the Task class"""

    def setUp(self):
        self.base_time = datetime.now()

        self.valid_task = Task(
            id=1,
            project_id=1,
            creator_id=1,
            title="Task Title",
            status=TaskStatus.OPEN,
            priority=TaskPriority.LOW,
            created_at=self.base_time,
            updated_at=self.base_time,
        )

    def test_task_creation_success(self):
        """Test the creation of a task"""
        task = Task(
            id=1,
            project_id=1,
            creator_id=1,
            title="Test Task",
            status=TaskStatus.OPEN,
            priority=TaskPriority.MEDIUM,
            created_at=self.base_time,
            updated_at=self.base_time,
        )
        self.assertEqual(task.title, "Test Task")

    def test_task_with_optional_fields(self):
        """Test the creation of a task with optional fields"""
        task = Task(
            id=2,
            project_id=1,
            creator_id=1,
            title="Optional Fields Task",
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            created_at=self.base_time,
            updated_at=self.base_time,
            assignee_id=2,
            deadline=datetime.now(),
            description="A detailed description",
        )
        self.assertIsNotNone(task.assignee_id)
        self.assertIsNotNone(task.deadline)
        self.assertIsNotNone(task.description)

    def test_invalid_id_type(self):
        """Test that an error is raised when an invalid ID type is provided"""
        with self.assertRaises(ValueError):
            Task(
                id="1",  # type: ignore
                project_id=1,
                creator_id=1,
                title="Test Task",
                status=TaskStatus.OPEN,
                priority=TaskPriority.MEDIUM,
                created_at=self.base_time,
                updated_at=self.base_time,
            )

    def test_invalid_priority_value(self):
        """Test that an error is raised when an invalid TaskPriority value is provided"""
        with self.assertRaises(ValueError):
            Task(
                id=2,
                project_id=1,
                creator_id=1,
                title="Test Task",
                status=TaskStatus.OPEN,
                priority="Medium", # type: ignore
                created_at=self.base_time,
                updated_at=self.base_time,
            )

    def test_priority_order(self):
        """Test the order of TaskPriority values"""
        low_priority_task = Task(
            id=3,
            project_id=1,
            creator_id=1,
            title="Low Priority",
            status=TaskStatus.DONE,
            priority=TaskPriority.LOW,
            created_at=self.base_time,
            updated_at=self.base_time,
        )
        high_priority_task = Task(
            id=4,
            project_id=1,
            creator_id=1,
            title="High Priority",
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            created_at=self.base_time,
            updated_at=self.base_time,
        )
        self.assertTrue(low_priority_task.priority < high_priority_task.priority)
        self.assertFalse(high_priority_task.priority < low_priority_task.priority)

    def test_failure_on_incorrect_datetime(self):
        """Test that an error is raised when an incorrect datetime is provided"""
        with self.assertRaises(ValueError):
            Task(
                id=5,
                project_id=1,
                creator_id=1,
                title="Date Type Test",
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.HIGH,
                created_at="2023-01-01T12:00:00",  # type: ignore
                updated_at=self.base_time,
            )

    def test_default_none_description(self):
        """Test that the description field is None by default"""
        self.assertIsNone(self.valid_task.description)

    def test_comparisons_between_priorities(self):
        """Test the comparison operators between TaskPriority values"""
        self.assertTrue(TaskPriority.LOW < TaskPriority.MEDIUM)
        self.assertTrue(TaskPriority.MEDIUM > TaskPriority.LOW)
        self.assertTrue(TaskPriority.HIGH >= TaskPriority.MEDIUM)
        self.assertTrue(TaskPriority.VERY_HIGH > TaskPriority.HIGH)
        self.assertTrue(TaskPriority.LOW <= TaskPriority.LOW)
        self.assertTrue(TaskPriority.LOW <= TaskPriority.MEDIUM)


class TestTaskService(unittest.TestCase):
    """Test the TaskService class"""

    def setUp(self):
        self.task_service = TaskService()
        self.task = Task(
            id=1,
            project_id=1,
            creator_id=1,
            title="Sample Task",
            status=TaskStatus.OPEN,
            priority=TaskPriority.LOW,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    @patch("protaskinate.repositories.task_repository.get_all")
    def test_get_all_by_project(self, mock_get_all):
        """Test the get_all_by_project method"""
        mock_get_all.return_value = [self.task]
        tasks = self.task_service.get_all_by_project(project_id=1)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Sample Task")

    @patch("protaskinate.repositories.task_repository.get")
    def test_get_by_id_and_project(self, mock_get):
        """Test the get_by_id_and_project method"""
        mock_get.return_value = self.task
        task = self.task_service.get_by_id_and_project(task_id=1, project_id=1)
        self.assertIsNotNone(task)
        if task is not None:
            self.assertEqual(task.id, 1)
            self.assertEqual(task.title, "Sample Task")

    @patch("protaskinate.repositories.task_repository.update")
    def test_update(self, mock_update):
        """Test the update method"""
        new_title = "Updated Task"
        mock_update.return_value = self.task

        self.task_service.update(task_id=1, project_id=1, title=new_title)

        mock_update.assert_called_with({"id": 1, "project_id": 1}, {"title": new_title})

    @patch("protaskinate.repositories.task_repository.create")
    def test_create(self, mock_create):
        """Test the create method"""
        mock_create.return_value = self.task
        created_task = self.task_service.create(
            title="New Task", priority=TaskPriority.HIGH
        )
        mock_create.assert_called_with(
            {"title": "New Task", "priority": TaskPriority.HIGH}
        )
        self.assertEqual(created_task, self.task)

    @patch("protaskinate.repositories.task_repository.delete")
    def test_delete(self, mock_delete):
        """Test the delete method"""
        self.task_service.delete(task_id=1, project_id=1)
        mock_delete.assert_called_with({"id": 1, "project_id": 1})

    @patch(
        "protaskinate.repositories.task_repository.count_by_assignee_grouped_by_status"
    )
    def test_count_by_assignee_grouped_by_status(
        self, mock_count_by_assignee_grouped_by_status
    ):
        """Test the count_by_assignee_grouped_by_status method"""
        mock_count_by_assignee_grouped_by_status.return_value = {TaskStatus.OPEN: 1}
        counts = self.task_service.count_by_assignee_grouped_by_status(assignee_id=1)
        self.assertEqual(counts[TaskStatus.OPEN], 1)
