from typing import Optional
from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

app = FastAPI()

# ------------------------------------------------------------------------------
# Request Model (Input)
# ------------------------------------------------------------------------------
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0)
    discount_price: Optional[float] = None
    quantity: int = Field(..., ge=0)
    category: str
    sku: str = Field(..., min_length=5, max_length=20)
    email: EmailStr
    stock: bool = True

    # 1. Clean name: remove leading/trailing spaces
    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return value.strip()

    # 2. Validate & format SKU: uppercase, no spaces allowed
    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value: str) -> str:
        if " " in value:
            raise ValueError("SKU-ში სფეისების (spaces) გამოყენება დაუშვებელია")
        return value.upper()

    # 3. Model Validator: check discount_price < price
    @model_validator(mode="after")
    def validate_discount_price(self) -> "ProductCreate":
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("ფასდაკლებული ფასი უნდა იყოს ჩვეულებრივ ფასზე ნაკლები")
        return self


# ------------------------------------------------------------------------------
# Response Model (Output) - Excludes `email` and `sku`
# ------------------------------------------------------------------------------
class ProductResponse(BaseModel):
    name: str
    price: float
    discount_price: Optional[float] = None
    quantity: int
    category: str
    stock: bool


# ------------------------------------------------------------------------------
# FastAPI Endpoints
# ------------------------------------------------------------------------------
@app.post(
    "/products/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="ახალი პროდუქტის დამატება"
)
def create_product(product: ProductCreate):
    return product

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_2:app", host="127.0.0.1", port=8000, reload=True)