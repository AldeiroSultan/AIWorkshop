from datetime import date
from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    INTERESTED = "Interested"
    PREPARING = "Preparing"
    SUBMITTED = "Submitted"
    SUCCESSFUL = "Successful"
    UNSUCCESSFUL = "Unsuccessful"


class Opportunity(BaseModel):
    id: int
    name: str
    organization: str = ""
    link: str | None = None
    amount: float | None = None  # CAD, None if unknown
    deadline: date
    status: Status = Status.INTERESTED
    owner: str = ""
    next_step: str = ""
