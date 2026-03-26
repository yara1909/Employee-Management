from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

# -----------------------------
# JWT settings
# -----------------------------
SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto") #using argon2 for password hashing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
#token url is the route where clients will send username/password to get token
#OAUth2 Password Bearer is a standard way to handle token-based authentication in FastAPI

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
# -----------------------------
# Hardcoded users
# -----------------------------
users = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("admin123"),  # Store hashed password
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password": pwd_context.hash("user123"),  # Store hashed password
        "role": "user"
    }
}

# -----------------------------
# Pydantic model
# -----------------------------
class Employee(BaseModel):
    id: int
    name: str
    position: str

# -----------------------------
# Tells FastAPI how to read token
# from Authorization: Bearer <token>
# -----------------------------

# -----------------------------
# Create JWT token
# -----------------------------
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# -----------------------------
# Login route
# Checks username/password
# Returns JWT token
# -----------------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get(form_data.username)

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={
            "sub": user["username"],
            "role": user["role"]
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# -----------------------------
# Decode and validate JWT token
# - checks signature
# - checks expiration
# - checks user exists
# Returns current user
# -----------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = users.get(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token user"
        )

    return user

# -----------------------------
# Admin-only dependency
# -----------------------------
def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

