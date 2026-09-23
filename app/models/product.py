from typing import Optional
from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, unique=True)
    description: Optional[str] = None
    price: float = Field(nullable=False)
    stock: int = Field(default=0, nullable=False)