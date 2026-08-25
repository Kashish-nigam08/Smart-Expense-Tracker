from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
class BudgetCreate(BaseModel):
    category: str
    budget_amount: float
    month: int
    year: int


class BudgetResponse(BaseModel):
    id: int
    category: str
    budget_amount: float
    month: int
    year: int

    class Config:
        from_attributes = True