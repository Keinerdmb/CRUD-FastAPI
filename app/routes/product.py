from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_session
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


def get_service(session: Session = Depends(get_session)) -> ProductService:
    return ProductService(session)


@router.get("/", response_model=List[ProductRead])
def list_products(service: ProductService = Depends(get_service)):
    return service.get_all()


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, service: ProductService = Depends(get_service)):
    return service.get_by_id(product_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, service: ProductService = Depends(get_service)):
    try:
        return service.create(data)
    except IntegrityError:
        raise HTTPException (status_code=status.HTTP_409_CONFLICT, detail="Product name already exists")
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid product data: {str(e)}")



@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, data: ProductUpdate, service: ProductService = Depends(get_service)):
    return service.update(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: ProductService = Depends(get_service)):
    service.delete(product_id)