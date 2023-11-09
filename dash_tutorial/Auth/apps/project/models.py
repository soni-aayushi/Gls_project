from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, ARRAY,func
from sqlalchemy.orm import relationship,validates
from config.settings import *
from apps.account.models import *



class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40 ), nullable=False)
    short_name = Column(String(3), nullable=False)  
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    # recipient = Column(ARRAY(String(length=255), dimensions=1), nullable=True)
    manage_by = Column(Integer, ForeignKey('users.id'))


    user = relationship("User", back_populates="projectsdv",foreign_keys=[manage_by])
    workflowstages = relationship("WorkFlowStages", back_populates="project_name")
    projectdevelopers = relationship("ProjectDeveloper", back_populates="project_name")  
    tasks = relationship("Tasks", back_populates="project_name")
    developers = relationship("User", secondary="project_developer", back_populates="projects")


project_developer = Table(
    "project_developer",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("developer_id", Integer, ForeignKey("users.id"))
)

class WorkFlowStages(Base):
    __tablename__ = "workflowstages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    project = Column(Integer, ForeignKey('projects.id'))
    project_name = relationship("Project", back_populates="workflowstages")
    Tasks = relationship("Tasks", back_populates="workflowstages")


class Role(Base):
    __tablename__ = "roles"
    id =Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    can_create_task = Column(Boolean, default=False)
    projectdevelopers = relationship("ProjectDeveloper", back_populates="roles")

class ProjectDeveloper(Base):
    __tablename__ = "projectdevelopers"

    id = Column(Integer, primary_key=True, index=True)
    project = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    created = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    developer = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    role = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'))
    project_name = relationship("Project", back_populates="projectdevelopers")
    user = relationship("User", back_populates="projectdevelopers",foreign_keys=[developer])
    roles = relationship("Role", back_populates="projectdevelopers")


class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    tasks = relationship("Tasks", back_populates="sprints")
  

class Tasks(Base):
    __tablename__ = "tasks"


    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=False)
    created_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime,nullable=True)
    estimate_time = Column(Boolean, default='00:00')
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime,nullable=True)
    assignee = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    project = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    sprint = Column(Integer, ForeignKey('sprints.id', ondelete='CASCADE')) 
    stage = Column(Integer, ForeignKey('workflowstages.id', ondelete='CASCADE'))
    created = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    deleted_by = Column(Integer, ForeignKey('users.id',ondelete='SET NULL'),nullable=True)

     

    user = relationship("User", back_populates="tasks",foreign_keys=[assignee])
    project_name = relationship("Project", back_populates="tasks")
    sprints = relationship("Sprint", back_populates="tasks")
    workflowstages = relationship("WorkFlowStages", back_populates="Tasks")
    user_create = relationship("User", back_populates="tasks_create",foreign_keys=[created])
    user_deleted_by = relationship("User", back_populates="tasks_deleted_by",foreign_keys=[deleted_by])





class TaskPlanner(Base):
    __tablename__ = "taskplanner"

    STATUS = {"new": "Inactive", "in_progress": "In progress", "complete": "Completed"}
    PRIORITIES = {1: "Eliminate", 2: "Delegate", 3: "Plan", 4: "Do"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=False)
    priority = Column(Integer,default=1)
    status = Column(String(6))
    created = Column(DateTime, default=func.now())
    user = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user_name = relationship("User", back_populates="taskplanner",foreign_keys=[user])

    @validates('priority')
    def validate_priority(self, key, value):
        if value not in self.PRIORITIES:
            raise ValueError(f"Invalid priority value: {value}")
        return value

    @validates('status')
    def validate_status(self, key, value):
        if value not in self.STATUS:
            raise ValueError(f"Invalid status value: {value}")
        return value

    
   

    




