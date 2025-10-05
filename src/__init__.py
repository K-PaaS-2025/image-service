from pydantic import BaseModel
import typing

class APIResponse(BaseModel):
    status: int
    status_text: str
    data: typing.Any
    message: str

class APIException(Exception):
    def __init__(self, response: APIResponse) -> None:
        self.response = response