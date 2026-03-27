from datetime import timedelta
from fastapi import HTTPException, status
from app.model.user_model import (
    get_user_by_username,
    create_user,
    update_user_activity,
)
from utils.utils import (
    hash_password,
    verify_password,
    create_access_token,
)


def register_new_user(user):
    
    # Check for duplicate username
    if get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username already exists"
        )

    user_dict = user.dict()

    user_dict["password"] = hash_password(user.password)
    user_dict["activity_log"] = []

    create_user(user_dict)
    
    update_user_activity(user.username, "User registered")

    return {"message": "User registered successfully"}


def login_user(user):
    db_user = get_user_by_username(user.username)

    if not db_user or not verify_password(user.password, db_user["password" ]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    update_user_activity(user.username, "User logged in")

    access_token = create_access_token(
        data={
            "username": db_user["username"],
            "role": db_user["role"]
        },
    )



    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user["role"] 
    }