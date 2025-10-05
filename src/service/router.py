from fastapi import APIRouter

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

router = APIRouter(
    prefix="/image-service",
    tags=["image-service"],
    responses={404: {"description": "Not found"}},
)

@router.get("/health", response_model=APIResponse)
async def health():
    return APIResponse(
        status=200,
        status_text="OK",
        data={"status": "healthy"},
        message="Service is healthy"
    )