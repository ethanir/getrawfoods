from pydantic import BaseModel, ConfigDict

from app.schemas.verification import VerificationRead


class FarmListItem(BaseModel):
    """A farm in the home-page list. Sufficient to render badges in each
    category section without a follow-up request.
    """

    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str
    location: str | None
    verifications: list[VerificationRead]


class FarmDetail(FarmListItem):
    """The full farm view returned from /farms/{slug}."""

    description: str
    website: str | None
    phone: str | None
    email: str | None
    sourcing_tips: str | None
