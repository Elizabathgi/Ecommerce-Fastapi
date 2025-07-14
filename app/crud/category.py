from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from fastapi import HTTPException, status

def create_category(db: Session, category: CategoryCreate):

    if not category.name or not category.name.strip():
        raise HTTPException(status_code=400, detail="Category name is required")
    # Sanitize name
    category.name = category.name.strip()
    # Check for duplicate
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = Category(**category.dict())
    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return JSONResponse(
             status_code=status.HTTP_201_CREATED,
            content={
                "status": 201,
                "message": "Category created successfully",
                "data": jsonable_encoder(new_category)
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

def get_all_categories(db: Session):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = { 
            "status" : 200,
            "message" : "success!",
            "data": jsonable_encoder(db.query(Category).all())
        }
    )
def update_category(db: Session, category_id: int, updates: CategoryUpdate):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"msg": "Category deleted"}
