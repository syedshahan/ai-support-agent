from fastapi import FastAPI

from app.api.routes.users import router as users_router
from app.api.routes.ai import router as ai_router


app = FastAPI()


app.include_router(users_router)
app.include_router(ai_router)
