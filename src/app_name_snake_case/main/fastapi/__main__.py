from app_name_snake_case.main.common.uvicorn import run_dev


def main() -> None:
    run_dev("app_name_snake_case.main.fastapi.asgi:app")


if __name__ == "__main__":
    main()
