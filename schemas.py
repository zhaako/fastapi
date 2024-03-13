from pydantic import BaseModel, ConfigDict


class STaskAdd(BaseModel):
    name: str
    description: str | None = None


class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class STaskUpdate(BaseModel):
    name: str
    description: str | None = None
