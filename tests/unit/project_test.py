"""tests/unit/project_test.py"""

import unittest
from datetime import datetime
from unittest.mock import patch

from protaskinate.entities.project import (
    Project,
    ProjectRole,
    ProjectUser,
    ProjectWithRole,
)
from protaskinate.entities.user import User
from protaskinate.services.project_service import ProjectService


class TestProjectEntity(unittest.TestCase):
    """Test Project entity"""

    def test_project_initialization(self):
        """Test correct initialization of Project dataclass."""
        project = Project(
            id=1,
            name="Test Project",
            description="A test project",
            creator_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.assertIsInstance(project, Project)
        self.assertEqual(project.id, 1)
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.description, "A test project")
        self.assertEqual(project.creator_id, 1)

    def test_project_with_invalid_types(self):
        """Test initialization with invalid types should raise TypeError."""
        with self.assertRaises(ValueError):
            Project(
                id="one",  # type: ignore
                name="Test Project",
                creator_id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )


class TestProjectWithRoleEntity(unittest.TestCase):
    """Test ProjectWithRole entity"""

    def test_project_with_role_initialization(self):
        """Test correct initialization of ProjectWithRole dataclass."""
        project = Project(
            id=1,
            name="Test Project",
            creator_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        project_with_role = ProjectWithRole(project=project, role=ProjectRole.ADMIN)
        self.assertIsInstance(project_with_role, ProjectWithRole)
        self.assertEqual(project_with_role.role, ProjectRole.ADMIN)


class TestProjectService(unittest.TestCase):
    """Test ProjectService class"""

    def setUp(self):
        self.project_service = ProjectService()
        self.project = Project(
            id=1,
            name="Test Project",
            creator_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.project_with_role = ProjectWithRole(
            project=self.project, role=ProjectRole.ADMIN
        )
        self.project_user = ProjectUser(
            user=User(id=1, username="test_user"), role=ProjectRole.ADMIN
        )

    @patch("protaskinate.services.project_service.project_repository.get_all")
    def test_get_all_projects(self, mock_get_all):
        """Test get all projects method."""
        mock_get_all.return_value = [self.project]
        projects = self.project_service.get_all()

        self.assertIsInstance(projects, list)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0], self.project)

    @patch(
        "protaskinate.services.project_service.project_repository.get_all_by_user_and_roles_with_role"
    )
    def test_get_all_by_user_with_role(self, mock_get_all_by_user):
        """Test fetching projects by user with specific roles."""
        user_id = 1
        mock_get_all_by_user.return_value = [self.project_with_role]
        projects = self.project_service.get_all_by_user_with_role(user_id)

        self.assertIsInstance(projects, list)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0], self.project_with_role)
        mock_get_all_by_user.assert_called_with(
            user_id, [ProjectRole.READER, ProjectRole.WRITER, ProjectRole.ADMIN]
        )

    @patch("protaskinate.services.project_service.project_repository.get")
    def test_get_project_by_id(self, mock_get):
        """Test get project by ID."""
        project_id = 1
        mock_get.return_value = self.project
        project = self.project_service.get_by_id(project_id)

        self.assertIsInstance(project, Project)
        self.assertEqual(project, self.project)
        mock_get.assert_called_with({"id": project_id})

    @patch("protaskinate.services.project_service.project_repository.delete")
    def test_delete_project(self, mock_delete):
        """Test delete project."""
        project_id = 1
        self.project_service.delete(project_id)
        mock_delete.assert_called_with({"id": project_id})

    @patch("protaskinate.services.project_service.project_repository.create")
    def test_create_project(self, mock_create):
        """Test creating a project."""
        project_data = {
            "id": 1,
            "name": "New Project",
            "creator_id": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        mock_create.return_value = Project(**project_data)
        project = self.project_service.create(**project_data)

        self.assertIsInstance(project, Project)
        self.assertEqual(project, Project(**project_data))
        mock_create.assert_called_with(project_data)

    @patch("protaskinate.services.project_service.project_repository.create_project_user")
    def test_add_user_to_project(self, mock_create_user):
        """Test adding user to project."""
        project_id, user_id, role = 1, 1, ProjectRole.ADMIN
        mock_create_user.return_value = self.project_user
        project_user = self.project_service.add_user(project_id, user_id, role)

        self.assertIsInstance(project_user, ProjectUser)
        self.assertEqual(project_user, self.project_user)
        mock_create_user.assert_called_with(project_id, user_id, role)


if __name__ == "__main__":
    unittest.main()
