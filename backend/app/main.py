from fastapi import FastAPI
from app.routers import test_router, data_router

app = FastAPI(title="Air Project API",
              description="Welcome to our Plant API",
              version="1.0.0",
              openapi_url="/openapi.json",
              docs_url="/docs",
              redoc_url="/redoc",)


app.include_router(test_router.test_router)

app.include_router(data_router.data_router)