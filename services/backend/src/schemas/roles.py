from pydantic import BaseModel


class ChangeRoleSchema(BaseModel):
    role: str
