from pydantic import BaseModel, Field, validator
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., example="Smartphone")
    description: Optional[str] = Field(None, example="Latest model smartphone")
    price: float = Field(..., gt=0, example=499.99)
    stock: int = Field(..., ge=0, example=50)
    category_id: int = Field(..., example=1)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
