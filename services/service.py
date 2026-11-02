from sqlalchemy.orm import Session
from model.task import Task
from model.User import User
from fastapi import HTTPException
from Authentication.JWTAuth import create_jwt_token, decode_jwt_token

def login_user(db: Session, login_data: User):

    try:
        data = db.query(User).filter(User.mobilenumber == login_data.mobilenumber, User.password == login_data.password).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    if not data:
        raise HTTPException(status_code=404, detail="User not found or invalid credentials")

    token = create_jwt_token(data.id)
    return token

def register_user(db: Session, register_data: User):

    if register_data.password != register_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    try:
        existing_user = db.query(User).filter(User.mobilenumber == register_data.mobilenumber).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while verifying your request: {e}")

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this mobile number already exists")

    new_user = User(
        username=register_data.username,
        mobilenumber=register_data.mobilenumber,
        password=register_data.password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while creating the user: {e}")

    return new_user

def create_task(db: Session, task_data: Task, decoded_user_id: int):


    new_task = Task(
        userid=decoded_user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    return new_task

def get_task(db: Session, task_id: int):
    try:
        task_data = db.query(Task).filter(Task.id == task_id).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_data

def update_task(db: Session, task_id: int, task_data: Task):
    try:
        existing_task = db.query(Task).filter(Task.id == task_id).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task.title = task_data.title
    existing_task.description = task_data.description
    existing_task.completed = task_data.completed

    try:
        db.commit()
        db.refresh(existing_task)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    return existing_task

def delete_task(db: Session, task_id: int):
    try:
        task_data = db.query(Task).filter(Task.id == task_id).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        db.delete(task_data)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    return {"detail": "Task deleted successfully"}

def get_all_tasks(db: Session):
    try:
        tasks = db.query(Task).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    return tasks

def get_completed_tasks(db: Session):
    try:
        tasks = db.query(Task).filter(Task.completed == True).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    if not tasks:
        raise HTTPException(status_code=404, detail="No completed tasks found")

    return tasks

def get_pending_tasks(db: Session):
    try:
        tasks = db.query(Task).filter(Task.completed == False).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred while processing your request: {e}")

    if not tasks:
        raise HTTPException(status_code=404, detail="No pending tasks found")

    return tasks

