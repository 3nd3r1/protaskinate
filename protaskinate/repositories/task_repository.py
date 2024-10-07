"""protaskinate/repositories/task_repository.py"""
from protaskinate.entities import Task
from protaskinate.repositories.repository import Repository

AllFields = ["id", "project_id", "creator_id", "title", "status", "priority", "created_at",
             "updated_at", "assignee_id", "deadline", "description"]
RequiredFields = ["project_id", "creator_id", "title", "status", "priority",
                  "created_at", "updated_at"]

def create_task_from_row(row) -> Task:
    """Helper function to create a Task entity from a database row"""
    return Task(id=row[0],
                project_id=row[1],
                creator_id=row[2],
                title=row[3],
                status=row[4],
                priority=row[5],
                created_at=row[6],
                updated_at=row[7],
                assignee_id=row[8],
                deadline=row[9],
                description=row[10])

class TaskRepository(Repository[Task]):
    """Task repository for managing tasks"""

    def __init__(self):
        super().__init__(table_name="tasks",
                         fields=AllFields,
                         required_fields=RequiredFields,
                         entity_creator=create_task_from_row)

task_repository = TaskRepository()
