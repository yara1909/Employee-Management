#Bootstrap employee management system
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.database import client, employees_collection
from app.routes.Employee_routes import router as employee_router
from app.routes.user_routes import router as user_routes
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        info = client.server_info()
        print("Connected to MongoDB:", info)
        print("Starting up the employee management system API...")

    except Exception as e:
        print("Error connecting to MongoDB:", e)
    yield

    print("Shutting down emplotee management system API...")
    

app = FastAPI(title="Employee Management System API", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins (not for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Include employee routes

app.include_router(employee_router, prefix="/employees")
app.include_router(user_routes, prefix="/auth")

#Health check endpoint 
@app.get("/")
def health_check():
    return {"status": "API is healthy"}