"""protaskinate/repositories/task_repository.py"""

import logging
from typing import Dict
from sqlalchemy import text
from protaskinate.entities import Task
from protaskinate.entities.task import TaskStatus
from protaskinate.repositories.repository import Repository
from protaskinate.utils.database import db

AllFields = [
    "id",
    "project_id",
    "creator_id",
    "title",
    "status",
    "priority",
    "created_at",
    "updated_at",
    "assignee_id",
    "deadline",
    "description",
]
RequiredFields = [
    "project_id",
    "creator_id",
    "title",
    "status",
    "priority",
    "created_at",
    "updated_at",
]


def create_task_from_row(row) -> Task:
    """Helper function to create a Task entity from a database row"""
    return Task(
        id=row[0],
        project_id=row[1],
        creator_id=row[2],
        title=row[3],
        status=row[4],
        priority=row[5],
        created_at=row[6],
        updated_at=row[7],
        assignee_id=row[8],
        deadline=row[9],
        description=row[10],
    )


class TaskRepository(Repository[Task]):
    """Task repository for managing tasks"""

    def __init__(self):
        super().__init__(
            table_name="tasks",
            fields=AllFields,
            required_fields=RequiredFields,
            entity_creator=create_task_from_row,
        )

    def count_by_assignee_grouped_by_status(
        self, assignee_id: int
    ) -> Dict[TaskStatus, int]:
        """Get all tasks assigned to a user grouped by status"""
        sql = """SELECT ts::text,  COALESCE(COUNT(task.id), 0)
                  FROM unnest(enum_range(NULL::task_status)) AS ts
                  LEFT JOIN tasks task ON task.status = ts AND task.assignee_id = :assignee_id
                  GROUP BY ts"""

        result = db.session.execute(text(sql), {"assignee_id": assignee_id})
        rows = result.fetchall()

        logging.info(rows)

        return {TaskStatus(row[0]): int(row[1]) for row in rows}


task_repository = TaskRepository()
