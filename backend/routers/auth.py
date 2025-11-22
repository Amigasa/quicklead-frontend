from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import db
from models import LoginRequest, Token, User
import hashlib

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    conn = db.get_connection()
    cursor = conn.cursor()
    
    user_id = credentials.credentials
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )
    
    return User(**user)

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Поиск пользователя по email или имени
    cursor.execute("""
        SELECT * FROM users 
        WHERE (email = %s OR name = %s) AND password = %s
    """, (login_data.username, login_data.username, hash_password(login_data.password)))
    
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )
    
    return Token(
        access_token=str(user["id"]),
        token_type="bearer",
        user=User(**user)
    )