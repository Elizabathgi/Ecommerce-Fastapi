from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., example="Electronics")
    description: str | None = Field(None, example="Devices and gadgets")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str | None = Field(None, example="Updated Name")
    description: str | None = Field(None, example="Updated description")

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True
