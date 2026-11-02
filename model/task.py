from sqlalchemy import Column, Integer, String, Boolean
from DB_connection import Base

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)