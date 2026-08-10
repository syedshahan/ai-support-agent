from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {"user_id": user_id}

@app.get("/users")
def get_users(limit: int = 10):
    return {"limit": limit}


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserCreate):
    return {
        "id": 1,
        "name": user.name,
        "email": user.email,
    }