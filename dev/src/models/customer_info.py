from pydantic import BaseModel, EmailStr


class CustomerInfo(BaseModel):
    handle: str
    forename: str
    surname: str
    email: EmailStr
