from sqlalchemy.orm import Session

from . import repositories
from .models import Student


class ValidationError(Exception):
    pass


def create_student(db: Session, name: str, email: str, age: int) -> Student:
    if not name.strip():
        raise ValidationError("name is required")
    if "@" not in email:
        raise ValidationError("email is not valid")
    if age < 0:
        raise ValidationError("age cannot be negative")
    if repositories.get_student_by_email(db, email) is not None:
        raise ValidationError("a student with that email already exists")

    return repositories.create_student(db, name=name, email=email, age=age)


def list_students(db: Session) -> list[Student]:
    return repositories.list_students(db)
