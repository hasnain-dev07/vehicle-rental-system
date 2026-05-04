from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel

# --- CONFIGURATION ---
SECRET_KEY = "jaan_secret_key_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- DATABASE SETUP ---
DATABASE_URL = "sqlite:///./rentals.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELS ---
class UserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

class VehicleTable(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    price_per_day = Column(Float)
    is_available = Column(Boolean, default=True)

# Pydantic Schema for Bulk Add
class VehicleCreate(BaseModel):
    brand: str
    model: str
    price_per_day: float

Base.metadata.create_all(bind=engine)

# --- UTILS & DEPENDENCIES ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(UserTable).filter(UserTable.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# --- API ENDPOINTS ---
app = FastAPI(title="Vehicle Rental System")

@app.post("/signup/")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    user_exists = db.query(UserTable).filter(UserTable.username == username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_pw = get_password_hash(password)
    new_user = UserTable(username=username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/profile/")
def get_profile(current_user: UserTable = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "role": "Admin" if current_user.is_admin else "Customer",
        "status": "Active"
    }

@app.get("/vehicles/")
def list_vehicles(
    brand: Optional[str] = None, 
    max_price: Optional[float] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(VehicleTable)
    if brand:
        query = query.filter(VehicleTable.brand.ilike(f"%{brand}%"))
    if max_price:
        query = query.filter(VehicleTable.price_per_day <= max_price)
    return query.all()

@app.post("/add-vehicle/")
def add_vehicle(brand: str, model: str, price: float, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="only admin can add the cars")
    new_vehicle = VehicleTable(brand=brand, model=model, price_per_day=price)
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

# 8. BULK ADD VEHICLES (Naya Feature ✨)
@app.post("/bulk-add-vehicles/")
def bulk_add_vehicles(
    vehicles: List[VehicleCreate], 
    db: Session = Depends(get_db), 
    current_user: UserTable = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="only admin can add the cars in bulk")
    
    added_count = 0
    for v in vehicles:
        new_v = VehicleTable(brand=v.brand, model=v.model, price_per_day=v.price_per_day)
        db.add(new_v)
        added_count += 1
    
    db.commit()
    return {"message": f"{added_count} cars are added succesfully"}

@app.put("/rent/{vehicle_id}")
def rent_car(vehicle_id: int, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    car = db.query(VehicleTable).filter(VehicleTable.id == vehicle_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="didnt get the car")
    if not car.is_available:
        raise HTTPException(status_code=400, detail="is already been rented")
    car.is_available = False
    db.commit()
    return {"message": f"{car.brand} {car.model} has been taken on rent"}

@app.delete("/vehicle/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only Admin can delete vehicles")
    car = db.query(VehicleTable).filter(VehicleTable.id == vehicle_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="didnt get the car")
    db.delete(car)
    db.commit()
    return {"message": f"{car.brand} {car.model} delete kar di gayi hai"}