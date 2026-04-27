from sqlalchemy.orm import Session

from .models import Student


def get_student_by_email(db: Session, email: str) -> Student | None:
    return db.query(Student).filter(Student.email == email).first()


def list_students(db: Session) -> list[Student]:
    return db.query(Student).all()


def create_student(db: Session, name: str, email: str, age: int) -> Student:
    student = Student(name=name, email=email, age=age)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
