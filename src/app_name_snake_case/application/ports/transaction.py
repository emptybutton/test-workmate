from contextlib import AbstractAsyncContextManager
from typing import Any


type Transaction = AbstractAsyncContextManager[Any]
