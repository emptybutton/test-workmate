from typing import Self

from pydantic import BaseModel, Field


class NoDataSchema(BaseModel): ...


class ErrorListSchema[ErrorSchemaT](BaseModel):
    error_models: tuple[ErrorSchemaT] = Field(alias="errors")


class ErrorSchema(BaseModel):
    def to_list(self) -> ErrorListSchema[Self]:
        return ErrorListSchema(errors=(self,))
