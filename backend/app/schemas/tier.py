from pydantic import BaseModel, ConfigDict


class TierRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str
    description: str | None
    display_order: int
