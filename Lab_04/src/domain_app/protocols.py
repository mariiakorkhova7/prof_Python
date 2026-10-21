from typing import Protocol, runtime_checkable

class HasId(Protocol):
    id: int

@runtime_checkable
class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None:
        ...