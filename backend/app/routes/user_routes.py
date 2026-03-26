from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserLogin, UserCreate
from app.controller.user_controller import register_new_user, login_user
from utils.utils import require_roles


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register(user_data:UserCreate):
    return register_new_user(user_data)


@router.post("/login")
def login(user_data: UserLogin):
    return login_user(user_data)

@router.get("/admin-dashboard", dependencies=[Depends(require_roles(["admin"]))])
def admin_dashboard():
    return {"message": "Welcome to the admin dashboard!"}

