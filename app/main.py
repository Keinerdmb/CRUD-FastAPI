from fastapi import FastAPI

from app.routes.product import router as product_router

app = FastAPI(title="Products API", version="1.0.0")

app.include_router(product_router)


@app.get("/")
def root():
    return {"status": "ok"}