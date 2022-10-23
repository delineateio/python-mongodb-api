from enum import Enum
from pydantic import BaseModel, Extra

class PhoneNumberType(str, Enum):
    WORK = "work"
    MOBILE = "mobile"
    HOME = "home"


class PhoneNumber(BaseModel, extra=Extra.forbid):
    Type: PhoneNumberType
    Number: str
