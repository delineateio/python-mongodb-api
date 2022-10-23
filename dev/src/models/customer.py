import datetime
from typing import List
from pydantic import BaseModel, EmailStr, validator, root_validator
from .phone_number import PhoneNumber
from .relationship import Relationship


class Customer(BaseModel):
    forename: str
    surname: str
    email: EmailStr
    birth_date: datetime.datetime
    handle: str
    phone_numbers: List[PhoneNumber]
    relationships: List[Relationship] | None

    # pylint: disable=no-self-argument
    @validator("handle")
    def check_handle_length(cls, data):
        if len(data) < 3:
            raise ValueError("the customer handle must be greater than 3 chars")
        return data

    # pylint: disable=no-self-argument
    @root_validator(pre=True)
    def set_handle(cls, data):

        handle = data.get("handle")
        if handle:
            data["handle"] = handle.lower()
        return data

    # pylint: disable=no-self-argument
    @root_validator(pre=True)
    def set_email(cls, data):

        email = data.get("email")
        if email:
            data["email"] = email.lower()
        return data
