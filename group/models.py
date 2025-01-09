import os
from typing import Optional, List
from datetime import datetime

from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

from message.models import UserModel
from core.models import BaseTimeModel


PyObjectId = Annotated[str, BeforeValidator(str)]


class Group(BaseTimeModel):
    """
    Container for a single group record.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default_factory=ObjectId, primary_key=True)
    user_id: PyObjectId = Field(default=None, foreign_key="UserModel._id")
    name: str = Field(...)
    dest_user_id: PyObjectId = Field(default=None, foreign_key="UserModel._id")
    media_url: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow) 
    text: str = Field(...)