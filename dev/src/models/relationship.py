from enum import Enum
from pydantic import BaseModel, Extra


class RelationshipType(str, Enum):
    MARRIED = "married"
    PARTNER = "parter"
    CHILD = "child"
    PARENT = "parent"


class Relationship(BaseModel, extra=Extra.forbid):
    of: RelationshipType
    to: str
