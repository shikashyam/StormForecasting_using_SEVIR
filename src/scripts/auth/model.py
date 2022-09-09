from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "jwt.",
                "content": "check for details"
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "sai raghavendra",
                "email": "sai@gmail.com",
                "password": "weakpassword"
            }
        }

class UserLoginSchema(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "sai@gmail.com",
                "password": "weakpassword"
            }
        }
