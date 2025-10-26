from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routers import plants_router

app = FastAPI(title="Air Project API",
              description="Welcome to our Plant API",
              version="1.0.0",
              openapi_url="/openapi.json",
              docs_url="/docs",
              redoc_url="/redoc",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(plants_router)
