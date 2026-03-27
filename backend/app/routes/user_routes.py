from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserLogin, UserCreate
from app.controller.user_controller import register_new_user, login_user
from utils.utils import require_roles


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register(user_data:UserCreate):
    return register_new_user(user_data)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = UserLogin(
        username=form_data.username,
        password=form_data.password
    )
    return login_user(user_data)

@router.get("/admin-dashboard", dependencies=[Depends(require_roles(["admin"]))])
def admin_dashboard():
    return {"message": "Welcome to the admin dashboard!"}

