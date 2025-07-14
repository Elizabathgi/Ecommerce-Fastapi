from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from app.crud import category as crud_category
from app.config.db import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud_category.create_category(db, category)

@router.get("/all", response_model=list[CategoryOut])
def get_all_categories(db: Session = Depends(get_db)):
    return crud_category.get_all_categories(db)

@router.patch("/{id}", response_model=CategoryOut)
def update_category(id: int, updates: CategoryUpdate, db: Session = Depends(get_db)):
    return crud_category.update_category(db, id, updates)

@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    return crud_category.delete_category(db, id)
