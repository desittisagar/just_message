import os
from typing import Optional, List
from datetime import datetime

from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from core.models import BaseTimeModel


PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseTimeModel):
    """
    Container for a single user record.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default_factory=ObjectId, primary_key=True)
    # id: ObjectId = Field(alias="_id", default_factory=ObjectId, primary_key=True)
    user_id: str = Field(...)
    username: str = Field(...)
    contact: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_id": "S123",
                "username": "Sagar",
                "contact": "+919999999990"
            }
        },
    )


class MessageModel(BaseTimeModel):
    """
    for a single message record - to be stored in background task
    """
    id: Optional[PyObjectId] = Field(alias="_id", default_factory=ObjectId, primary_key=True)
    source_user_id: PyObjectId = Field(default=None, foreign_key="UserModel._id")
    dest_user_id: PyObjectId = Field(default=None, foreign_key="UserModel._id")
    media_url: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow) 
    text: str = Field(...)