from fastapi import FastAPI
from routers import router
from DB_connection import Base, engine
from model.task import Task
from model.User import User
from routers.router import router

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Task Manager Application")
app.include_router(router)