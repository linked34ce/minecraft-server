from dataclasses import dataclass
from typing import Literal, Optional, TypedDict


class MinecraftApiResponse(TypedDict):
    statusCode: int
    status: Literal["success", "error"]
    message: Optional[str]
    is_running: Optional[bool]
    ip_address: Optional[str]


@dataclass
class FuncResult():
    is_successful: bool
    data: Optional[dict] = None
    response: Optional[MinecraftApiResponse] = None
