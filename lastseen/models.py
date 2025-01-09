import os
from typing import Optional, List
from datetime import datetime

from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from core.models import BaseTimeModel
from message.models import UserModel


PyObjectId = Annotated[str, BeforeValidator(str)]

class UnsentMessageModel(BaseTimeModel):
    """
    for a single message record - to be stored in background task
    """
    id: Optional[PyObjectId] = Field(alias="_id", default_factory=ObjectId, primary_key=True)
    source_user_id: PyObjectId = Field(default=None, foreign_key="UserModel._id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)