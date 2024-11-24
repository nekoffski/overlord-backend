import dataclasses
from typing import List


@dataclasses.dataclass
class DeviceInfo(object):
    id: int
    model: str
    name: str
    host: str
    port: int
    actions: list[str]

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return other.id == self.id

    def supports_action(self, action: str) -> bool:
        return action in self.actions
