from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

def create_product(db: Session, product: ProductCreate):
    # Check if category exists
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check for duplicate product name
    existing = db.query(Product).filter(Product.name == product.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")

    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return  JSONResponse(
             status_code=status.HTTP_201_CREATED,
            content={
                "status": 201,
                "message": "Product created successfully",
                "data": jsonable_encoder(new_product)
            }
        )



def get_all_products(db: Session):
    products = db.query(Product).options(joinedload(Product.category)).all()
    
    result = []
    for product in products:
        item = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category": {
                "id": product.category.id,
                "name": product.category.name
            }
        }
        result.append(item)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": 200,
            "message": "success!",
            "data": result
        }
    )



from sqlalchemy.orm import joinedload

def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).options(joinedload(Product.category)).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "category": {
            "id": product.category.id,
            "name": product.category.name
        }
    }

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": 200,
            "message": "Product fetched successfully",
            "data": product_data
        }
    )




def get_products_by_category(db: Session, category_id: int):
    products = db.query(Product).options(joinedload(Product.category)).filter(Product.category_id == category_id).all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found in this category")

    result = []
    for product in products:
        item = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category": {
                "id": product.category.id,
                "name": product.category.name
            }
        }
        result.append(item)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": 200,
            "message": "Products fetched successfully",
            "data": result
        }
    )


def update_product(db: Session, product_id: int, updates: ProductUpdate):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if updates.category_id:
        category = db.query(Category).filter(Category.id == updates.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="New category not found")

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": 200,
            "message": "Product updated successfully",
            "data": jsonable_encoder(product)
        }
    )

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"msg": "Product deleted"}
