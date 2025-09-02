from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserCreateByAdmin(UserCreate):
    role: str = "staff"

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str