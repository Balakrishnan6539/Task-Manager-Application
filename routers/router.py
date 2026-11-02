from fastapi import APIRouter,Depends,Cookie,Response
from sqlalchemy.orm import Session

from DB_connection import get_db
from services import service
from schemas.schema import Task, Login, Register, RegisterResponse, LoginResponse
from Authentication.JWTAuth import check_the_user

router = APIRouter()

@router.post("/login", response_model=  LoginResponse)
def login_user(login_data: Login,response: Response, db: Session = Depends(get_db)):
    token=service.login_user(db, login_data)
    response.set_cookie(key="token", value=token, httponly=True)
    print("Token set in cookie:", token)
    return {"token": token}

@router.post("/register", response_model=RegisterResponse)
def register_user(register_data: Register, db: Session = Depends(get_db)):
    return service.register_user(db, register_data) 

@router.post("/task", response_model=Task)
def create_task(task_data: Task,id: int =Depends(check_the_user), db: Session = Depends(get_db)):
    return service.create_task(db, task_data,id)

@router.get("/task/{task_id}", response_model=Task, dependencies=[Depends(check_the_user)])
def get_task(task_id: int, db: Session = Depends(get_db)):
    return service.get_task(db, task_id)

@router.get("/tasks", response_model=list[Task],dependencies=[Depends(check_the_user)])
def get_all_tasks(db: Session = Depends(get_db)):
    return service.get_all_tasks(db)

@router.put("/task/{task_id}", response_model=Task,dependencies=[Depends(check_the_user)])
def update_task(task_id: int, task_data: Task, db: Session = Depends(get_db)):
    return service.update_task(db, task_id, task_data)

@router.delete("/task/{task_id}",dependencies=[Depends(check_the_user)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return service.delete_task(db, task_id)

@router.get("/tasks/completed", response_model=list[Task],dependencies=[Depends(check_the_user)])
def get_completed_tasks(db: Session = Depends(get_db)):
    return service.get_completed_tasks(db)

@router.get("/tasks/pending", response_model=list[Task],dependencies=[Depends(check_the_user)])
def get_pending_tasks(db: Session = Depends(get_db)):
    return service.get_pending_tasks(db)

