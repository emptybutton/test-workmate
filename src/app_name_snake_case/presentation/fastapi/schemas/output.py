from typing import Literal

from pydantic import BaseModel

from app_name_snake_case.presentation.fastapi.schemas.common import ErrorSchema


class UserSchema(BaseModel):
    name: str


class AlreadyRegisteredUserSchema(ErrorSchema):
    type: Literal["alreadyRegisteredUser"] = "alreadyRegisteredUser"


class AlreadyTakenUserNameSchema(ErrorSchema):
    type: Literal["alreadyTakenUserName"] = "alreadyTakenUserName"
