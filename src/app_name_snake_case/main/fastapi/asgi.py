from app_name_snake_case.main.common.asgi import LazyASGIApp
from app_name_snake_case.main.fastapi.di import container
from app_name_snake_case.presentation.fastapi.app import app_from


app = LazyASGIApp(app_factory=lambda: app_from(container))
