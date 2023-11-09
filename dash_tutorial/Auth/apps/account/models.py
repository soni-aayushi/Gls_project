
from sqlalchemy import Column, Integer, String,Boolean, DateTime, func
from sqlalchemy.orm import relationship
from config.settings import *
from apps.project.models import *

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    projectsdv = relationship("Project", back_populates="user",foreign_keys=[Project.manage_by])
    projectdevelopers = relationship("ProjectDeveloper", back_populates="user",foreign_keys=[ProjectDeveloper.developer])
    tasks = relationship("Tasks", back_populates="user",foreign_keys=[Tasks.assignee])
    tasks_create = relationship("Tasks", back_populates="user_create",foreign_keys=[Tasks.created])
    tasks_deleted_by = relationship("Tasks", back_populates="user_deleted_by",foreign_keys=[Tasks.deleted_by])
    taskplanner = relationship("TaskPlanner", back_populates="user_name",foreign_keys=[TaskPlanner.user])
    projects = relationship("Project", secondary="project_developer", back_populates="developers")








class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=func.now())

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    email = Column(String, primary_key=True)
    reset_token = Column(String)
    reset_token_expiry = Column(DateTime)