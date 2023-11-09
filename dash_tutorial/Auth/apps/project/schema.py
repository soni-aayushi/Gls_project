from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from apps.account.models import *



class PojectCreate(BaseModel):
    name: str
    short_name: str
    start_date: str
    end_date: str
    is_active: bool  # Use 'bool' instead of 'Boolean'
    # recipient: Optional[List[str]] = []
    manage_by: int

    
class ProjectResponse(BaseModel):
    id: int
    name: str
    short_name: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    # recipient: list
    manage_by: int

class ProjectCreate(PojectCreate):
    pass

class ProjectUpdate(PojectCreate):
    pass

class MessageResponse(BaseModel):
    message: str
    
class ProjectInDB(PojectCreate):
    id: int

class ProjectOut(ProjectInDB):
    pass

class CustomBooleanField(BaseModel):
    # Custom Pydantic model for handling SQLAlchemy Boolean type
    value: bool

# Use CustomBooleanField in the ProjectBase model
class ProjectBaseWithCustomBoolean(PojectCreate):
    is_active: CustomBooleanField

#workflow
class CreateWorkflowstages(BaseModel):
    name :str
    id : int 

class WorkflowStageResponse(BaseModel):
    id: int
    name: str
    id: int

class WorkflowStageInDB(CreateWorkflowstages):
    id: int

class WorkflowStageOut(WorkflowStageInDB):
    pass

class WorkflowStageListResponse(BaseModel):
    items: List[WorkflowStageResponse]



class Role(BaseModel):
    name :str
    can_create_task : bool


class ProjectDeveloper(BaseModel):
    project : int
    created : datetime
    is_active : bool
    developer : int
    role : int


class Sprint(BaseModel):
    name :str
    description :str
    start_date : datetime
    end_date : datetime


class Taskcreate(BaseModel):
    title :str
    created_at : datetime
    resolved_at : datetime
    estimate_time : bool
    is_deleted : datetime
    assignee : int
    project : int
    sprint : int
    status : int
    created : int
    deleted_by : int


class TaskPlanner(BaseModel):
    title : str
    priority : int
    status : int
    created : datetime
    user : int