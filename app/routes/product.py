from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_session
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


def get_service(session: Session = Depends(get_session)) -> ProductService:
    return ProductService(session)


@router.get("/", response_model=List[ProductRead])
def list_products(
    skip: int = Query(default=0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(default=100, ge=1, le=100, description="Número máximo de registros a retornar"),
    service: ProductService = Depends(get_service),
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, service: ProductService = Depends(get_service)):
    return service.get_by_id(product_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, service: ProductService = Depends(get_service)):
    try:
        return service.create(data)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product name already exists")


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, data: ProductUpdate, service: ProductService = Depends(get_service)):
    try:
        return service.update(product_id, data)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product name already exists")


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: ProductService = Depends(get_service)):
    service.delete(product_id)