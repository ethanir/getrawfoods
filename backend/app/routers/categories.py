from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Category
from app.schemas import CategoryRead

router = APIRouter()


@router.get("/categories", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)) -> list[Category]:
    stmt = select(Category).order_by(Category.display_order)
    return list(db.scalars(stmt))
