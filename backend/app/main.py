from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .database.database import SessionLocal, engine, Base
from .routers import plants_router, question_router, recommendations_router, user_study_router
from .services import store_csv_entries_to_db, store_questions_to_db, store_answer_options_to_db


# For loading data to the database once upon startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        store_csv_entries_to_db(db=db)
        store_questions_to_db(db=db)
        store_answer_options_to_db(db=db)
    finally:
        db.close()
    yield

app = FastAPI(title="Air Project API",
              description="Welcome to our Plant API",
              version="1.0.0",
              openapi_url="/openapi.json",
              docs_url="/docs",
              redoc_url="/redoc",
              lifespan=lifespan
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This could be commented out, it is needed only once for creating the tables
Base.metadata.create_all(bind=engine)

app.include_router(plants_router)

app.include_router(question_router)

app.include_router(recommendations_router)

app.include_router(user_study_router)
