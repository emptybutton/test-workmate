from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from app_name_snake_case.application.view_user import ViewUser
from app_name_snake_case.presentation.fastapi.cookies import UserIDCookie
from app_name_snake_case.presentation.fastapi.schemas.output import UserSchema
from app_name_snake_case.presentation.fastapi.tags import Tag


view_user_router = APIRouter()


class RegisterUserSchema(BaseModel):
    user_name: str = Field(alias="userName")


@view_user_router.get(
    "/user",
    responses={
        status.HTTP_200_OK: {"model": UserSchema},
        status.HTTP_204_NO_CONTENT: {},
    },
    summary="View user",
    description="View current user.",
    tags=[Tag.user],
)
@inject
async def view_user_route(
    view_user: FromDishka[ViewUser[str, UserSchema, UserSchema | None]],
    signed_user_id: UserIDCookie.StrOrNone = None,
) -> Response:
    view = await view_user(signed_user_id=signed_user_id)

    if view is None:
        return Response(b"", status_code=status.HTTP_204_NO_CONTENT)

    response_body = view.model_dump(mode="json", by_alias=True)
    return JSONResponse(response_body)
