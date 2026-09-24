from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.product import router as product_router

app = FastAPI(
    title="Products API",
    description="API RESTful para la gestión y control de productos con FastAPI y SQLModel",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)


@app.get("/")
def root():
    return {"status": "ok"}