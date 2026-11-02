from pydantic import Field
from schemas.Validator import FieldValidatorClass


class Login(FieldValidatorClass):
    mobilenumber: str = Field(...,min_length=10,max_length=10)
    password: str =Field(...,min_length=8,max_length=50)


class Register(FieldValidatorClass):
    username: str = Field(...,min_length=3,max_length=50)
    mobilenumber: str = Field(...,min_length=10,max_length=10)
    password: str = Field(...,min_length=8,max_length=50)
    confirm_password: str = Field(...,min_length=8,max_length=50)


class Task(FieldValidatorClass):
    title: str = Field(...,min_length=2,max_length=100)
    description: str = Field(None, min_length=2,max_length=500)
    completed: bool = Field(default=False)


class LoginResponse(FieldValidatorClass):
    token: str
    
class RegisterResponse(FieldValidatorClass):
    username: str
    mobilenumber: str

