import os
from fastapi import FastAPI, Security, Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

# ---- Cargar Variables ----
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ---- Iniciar App ----
app = FastAPI(title="Tarea3_PCD_USERS", version="1.0.0")

# ---- Crear Tablas ---- 
models.Base.metadata.create_all(bind=engine)

# ---- Dependencia DB ---- 
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ---- Seguridad por Header ----
api_key_header = APIKeyHeader(name="X-API-Key", description="API key por header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# ---- Esquema Pydantic ---- 
class User(BaseModel):
    user_name: str = Field(min_length=1, max_length=100)
    user_email: str = Field(min_length=1, max_length=100)
    age: int | None = None
    recommendations: list[str] = Field(default_factory=list)
    zip: int | None = None

@app.get("/")
def root():
    return {"message": "user api up. see /Docs"}

# ---- Endpoint Protegido ----
@app.get("/api/v1/secure-data/", tags=["secure"])
async def secure_data(api_key: str = Depends(get_api_key)):
    return {"message": "Secure data access granted."}

# ---- Endpoints ----
@app.post("/api/v1/users/", tags=["users"])
def create_user(users: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    email_already_on_file = db.query(models.User).filter(models.User.user_email == users.user_email).first()
    if email_already_on_file:
        raise HTTPException(status_code=400, detail="That email is already on use")
    db_user = models.User(
        user_name=users.user_name,
        user_id=users.user_id,
        user_email=users.user_email,
        age=users.age,
        recommendations=users.recommendations,
        zip=users.zip
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/api/v1/users/{user_id}", tags=["users"])
def update_user(user_id: int, users: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_user = db.query(models.User).filter(models.User.user == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")
    
    db_user.user_name = users.user_name
    db_user.user_email = users.user_email
    db_user.age = users.age
    db_user.recommendations = users.recommendations
    db_user.zip = users.zip

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/v1/users/{user_id}", tags=["users"])
def list_users(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    return db.query(models.User).all()

@app.delete("/api/v1/users/{user_id}", tags=["users"])
def delete_user(user_id: int, users: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_user = db.query(models.User).filter(models.User.user == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")
    
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return {"deleted_id": user_id}