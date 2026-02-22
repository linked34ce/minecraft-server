from dataclasses import dataclass
from typing import Literal, Optional, TypedDict


class MinecraftServerStatus(TypedDict):
    isRunning: bool
    ipAddress: Optional[str]


class MinecraftApiResponse(TypedDict):
    statusCode: int
    status: Literal["success", "error"]
    message: Optional[str] = None
    serverStatus: Optional[MinecraftServerStatus] = None


@dataclass
class FuncResult():
    is_successful: bool
    data: Optional[dict] = None
    response: Optional[MinecraftApiResponse] = None
