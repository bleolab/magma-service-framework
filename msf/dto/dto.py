from pydantic import BaseModel

class RequestDTO(BaseModel):
    request: str
    transaction: str
    action: str
    payload: str

class ResponseDTO(BaseModel):
    request: str
    transaction: str
    status: str
    message: str