from typing import List
from sqlmodel import Session, select

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.exceptions import ProductNotFoundException, InvalidStockException, ProductAlreadyExistsException


class ProductService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Product]:
        return self.session.exec(select(Product)).all()

    def get_by_id(self, product_id: int) -> Product:
        product = self.session.get(Product, product_id)
        if not product:
            raise ProductNotFoundException(product_id)
        return product

    def create(self, data: ProductCreate) -> Product:
        if data.stock < 0:
            raise InvalidStockException(detail="El stock no puede ser negativo")

        existing = self.session.exec(
            select(Product).where(Product.name == data.name)
        ).first()
        if existing:
            raise ProductAlreadyExistsException(data.name)

        product = Product(**data.model_dump())
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def update(self, product_id: int, data: ProductUpdate) -> Product:
        product = self.get_by_id(product_id)
        update_data = data.model_dump(exclude_unset=True)

        if "stock" in update_data and update_data["stock"] < 0:
            raise InvalidStockException()

        for key, value in update_data.items():
            setattr(product, key, value)

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: int) -> None:
        product = self.get_by_id(product_id)
        self.session.delete(product)
        self.session.commit()