from typing import TypedDict, NotRequired

class StudentPayload(TypedDict):
    id: int
    name: str
    group: str
    email: NotRequired[str]