from dataclasses import dataclass
from typing import List, Optional


@dataclass
class UserInfo:
    username: str
    doc: Optional[str]
    active: bool
    email_verified: bool
    roles: List[str]
