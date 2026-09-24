from typing import Optional
from sqlmodel import SQLModel
from pydantic import Field


class ProductCreate(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(ge=0, default=0, description="El stock no puede ser negativo")


class ProductUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0, description="El precio debe ser mayor a 0")
    stock: Optional[int] = Field(default=None, ge=0, description="El stock no puede ser negativo")


class ProductRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int