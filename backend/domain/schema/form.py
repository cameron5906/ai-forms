from uuid import UUID
import uuid
from sqlmodel import SQLModel, Field

class FormResponse(SQLModel):
    """DTO for sending form data to the UI"""
    id: UUID
    title: str

    class Config:
        from_attributes = True  # This enables mapping from ORM objects

class FormBase(SQLModel):
    id: UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    title: str = Field(nullable=False)

class Form(FormBase, table=True):
    """
    SQLAlchemy model representing a form in the database.
    
    Attributes:
        id (UUID): Unique identifier for the form
        title (str): Title of the form
        form_information (str): JSON structure storing form information
    """
    __tablename__ = "forms"
    
    form_information: str = Field(nullable=False)
    
class FormValue(SQLModel, table=True):
    __tablename__ = "form_values"
    
    id: UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    form_id: UUID = Field(foreign_key="forms.id")
    session_id: UUID = Field(foreign_key="chat_sessions.id")
    field_id: str = Field(nullable=False)
    value: str = Field(nullable=False)