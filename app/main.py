from fastapi import FastAPI
from app.config.db import Base, engine
from app.routes import product, category

app = FastAPI(title="E-commerce API")

# Create DB tables
Base.metadata.create_all(bind=engine)

# Register routers
@app.get("/")
def root():
    return {"message": " E-commerce API is running"}


app.include_router(product.router, prefix="/api/products", tags=["Products"])
app.include_router(category.router, prefix="/api/category", tags=["Categories"])
