from typing import Optional
from sqlmodel import SQLModel


class ProductCreate(SQLModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


class ProductRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int