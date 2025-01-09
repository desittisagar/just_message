from datetime import datetime

from pydantic import BaseModel, Field


class BaseTimeModel(BaseModel):
    """Base model for all models with created_at and updated_at fields."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)