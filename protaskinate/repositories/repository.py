"""protaskinate/repositories/repository.py"""
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

from sqlalchemy import Row, text

from protaskinate.utils.database import db

T = TypeVar("T")

class Repository(Generic[T]):
    """Generic base repository class for common CRUD operations"""

    def __init__(self, table_name: str, fields: List[str],
                 required_fields: List[str], entity_creator: Callable[[Row[Any]], T]):
        self._table_name = table_name
        self._fields = fields
        self._required_fields = required_fields
        self._entity_creator = entity_creator

    def get_all(self, by_fields: Optional[Dict[str, Union[int, str]]] = None,
                order_by_fields: Optional[List[str]] = None,
                reverse: Optional[List[bool]] = None) -> List[T]:
        """Get all entities from the repository by some fields"""
        if by_fields is not None:
            if any(key not in self._fields for key in by_fields):
                raise ValueError("Invalid by fields")
        if order_by_fields is not None:
            if any(field not in self._fields for field in order_by_fields):
                raise ValueError("Invalid order by fields")
            if reverse is None or len(order_by_fields) != len(reverse):
                raise ValueError("Invalid reverse fields")

        order_clause = ""
        where_clause = ""
        all_fields = ", ".join(self._fields)
        if order_by_fields is not None and reverse is not None:
            order_clause = "ORDER BY " + ", ".join(
                f"{field} {'DESC' if rev else ''}"
                for field, rev in zip(order_by_fields, reverse)
            )
        if by_fields is not None:
            where_clause = "WHERE " + " AND ".join(f"{key} = :{key}" for key in by_fields)

        sql = f"SELECT {all_fields} FROM {self._table_name} {where_clause} {order_clause}"
        result = db.session.execute(text(sql), by_fields)
        rows = result.fetchall()

        return [self._entity_creator(row) for row in rows]

    def get(self, by_fields: Dict[str, Union[int, str]]) -> Optional[T]:
        """Get one entity from the repository by some fields"""
        if any(key not in self._fields for key in by_fields):
            raise ValueError("Invalid by fields")

        where_clause = "WHERE " + " AND ".join(f"{key} = :{key}" for key in by_fields)
        all_fields = ", ".join(self._fields)

        sql = f"SELECT {all_fields} FROM {self._table_name} {where_clause}"

        result = db.session.execute(text(sql), by_fields)
        row = result.fetchone()

        return self._entity_creator(row) if row else None

    def create(self, **kwargs) -> Optional[T]:
        """Create a new entity in the repository"""
        if any(key not in self._fields for key in kwargs):
            raise ValueError("Invalid fields")
        if not all(key in kwargs for key in self._required_fields):
            raise ValueError("Missing required fields")

        fields = ", ".join(kwargs.keys())
        values = ", ".join(f":{key}" for key in kwargs)
        all_fields = ", ".join(self._fields)

        sql = f"INSERT INTO {self._table_name} ({fields}) VALUES ({values}) RETURNING {all_fields}"

        result = db.session.execute(text(sql), kwargs)
        row = result.fetchone()
        db.session.commit()

        return self._entity_creator(row) if row else None

    def update(self, entity_id: int, **kwargs) -> Optional[T]:
        """Update an entity in the repository"""
        if not kwargs or any(key not in self._fields for key in kwargs):
            raise ValueError("Invalid update fields")

        set_clause = ", ".join(f"{key} = :{key}" for key in kwargs)
        all_fields = ", ".join(self._fields)

        sql = f"""UPDATE {self._table_name}
                  SET {set_clause} WHERE id = :entity_id RETURNING {all_fields}"""

        result = db.session.execute(text(sql), {"entity_id": entity_id, **kwargs})
        row = result.fetchone()
        db.session.commit()

        return self._entity_creator(row) if row else None
