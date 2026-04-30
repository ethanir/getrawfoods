from pydantic import BaseModel


class VerificationRead(BaseModel):
    """A single (category, tier) badge attached to a farm.

    Slugs rather than IDs because the API consumer cares about stable
    identifiers, not internal primary keys.
    """

    category: str
    tier: str
