from fastapi import FastAPI
from sqlalchemy import inspect
from starlette.middleware.cors import CORSMiddleware
from .database import Base
from .database.database import engine
from .routers import plants_router
from .models import Plant

# Use when you add new tables
# Base.metadata.create_all(bind=engine)


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


# inspector = inspect(engine)
# print("Tables:", inspector.get_table_names())
app.include_router(plants_router)
