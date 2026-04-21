from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username minimal 3 karakter")
    password: str = Field(..., min_length=6, max_length=100, description="Password minimal 6 karakter")


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
