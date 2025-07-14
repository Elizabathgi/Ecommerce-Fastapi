from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.crud import product as crud_product
from app.config.db import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, product)

@router.get("/all", response_model=list[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    return crud_product.get_all_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return crud_product.get_product_by_id(db, product_id)

@router.get("/category/{category_id}", response_model=list[ProductOut])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    return crud_product.get_products_by_category(db, category_id)

@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, updates: ProductUpdate, db: Session = Depends(get_db)):
    return crud_product.update_product(db, product_id, updates)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud_product.delete_product(db, product_id)
