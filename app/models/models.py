
from typing import List
from app.engine import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class People(Base):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)

    items: Mapped[List["Items"]] = relationship(back_populates="person")
    enrollments: Mapped[List["Enrollments"]] = relationship(back_populates="person")

class Items(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(String)
    people_id: Mapped[People] = relationship()

    person: Mapped["People"] = relationship(back_populates="items")

class Courses(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str] = mapped_column(String)

    enrollments: Mapped[List["Enrollments"]] = relationship(back_populates="course")


class Enrollments(Base):
    __tablename__ = "enrollments"
    people_id: Mapped[People] = relationship()
    course_id: Mapped[Courses] = relationship()

    person: Mapped["People"] = relationship(back_populates="enrollments")
    course: Mapped["Courses"] = relationship(back_populates="enrollments")