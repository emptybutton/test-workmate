from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from app_name_snake_case.application.register_user import (
    RegisteredUserToRegisterUserError,
    RegisterUser,
    TakenUserNameToRegisterUserError,
)
from app_name_snake_case.presentation.fastapi.cookies import (
    UserIDCookie,
)
from app_name_snake_case.presentation.fastapi.schemas.common import (
    ErrorListSchema,
    NoDataSchema,
)
from app_name_snake_case.presentation.fastapi.schemas.output import (
    AlreadyRegisteredUserSchema,
    AlreadyTakenUserNameSchema,
    UserSchema,
)
from app_name_snake_case.presentation.fastapi.tags import Tag


register_user_router = APIRouter()


class RegisterUserSchema(BaseModel):
    user_name: str = Field(alias="userName")


@register_user_router.post(
    "/user",
    responses={
        status.HTTP_201_CREATED: {"model": NoDataSchema},
        status.HTTP_409_CONFLICT: {
            "model": (
                ErrorListSchema[AlreadyRegisteredUserSchema]
                | ErrorListSchema[AlreadyTakenUserNameSchema]
            )
        },
    },
    summary="Register user",
    description="Register current user.",
    tags=[Tag.user],
)
@inject
async def register_user_route(
    register_user: FromDishka[RegisterUser[str, UserSchema, UserSchema | None]],
    request_body: RegisterUserSchema,
    signed_user_id: UserIDCookie.StrOrNone = None,
) -> Response:
    try:
        result = await register_user(
            signed_user_id=signed_user_id, user_name=request_body.user_name
        )
    except RegisteredUserToRegisterUserError:
        response_body = (
            AlreadyRegisteredUserSchema()
            .to_list()
            .model_dump(mode="json", by_alias=True)
        )
        return JSONResponse(response_body, status_code=status.HTTP_409_CONFLICT)
    except TakenUserNameToRegisterUserError:
        response_body = (
            AlreadyTakenUserNameSchema()
            .to_list()
            .model_dump(mode="json", by_alias=True)
        )
        return JSONResponse(response_body, status_code=status.HTTP_409_CONFLICT)

    response_body = result.user_view.model_dump(mode="json", by_alias=True)
    response = JSONResponse(response_body, status_code=status.HTTP_201_CREATED)

    cookie = UserIDCookie(response)
    cookie.set(result.signed_user_id)

    return response
