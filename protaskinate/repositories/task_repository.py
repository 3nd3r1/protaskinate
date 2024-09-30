"""protaskinate/repositories/task_repository.py"""
from protaskinate.entities import Task
from protaskinate.repositories.repository import Repository

AllFields = ["id", "title", "status", "creator_id", "created_at", "priority",
             "assignee_id", "deadline", "project_id"]
RequiredFields = ["title", "status", "creator_id", "created_at", "priority", "project_id"]

def create_task_from_row(row) -> Task:
    """Helper function to create a Task entity from a database row"""
    return Task(id=row[0],
                title=row[1],
                status=row[2],
                creator_id=row[3],
                created_at=row[4],
                priority=row[5],
                assignee_id=row[6],
                deadline=row[7],
                project_id=row[8])

class TaskRepository(Repository[Task]):
    """Task repository for managing tasks"""

    def __init__(self):
        super().__init__(table_name="tasks",
                         fields=AllFields,
                         required_fields=RequiredFields,
                         entity_creator=create_task_from_row)

task_repository = TaskRepository()
