from fastapi import APIRouter, Depends, HTTPException
from database import db
from models import User, UserCreate
from routers.auth import get_current_user, hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[User])
async def get_users(current_user: User = Depends(get_current_user)):
    if current_user.role != "администратор":
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role FROM users WHERE role != 'клиент' ORDER BY id")
    users = cursor.fetchall()
    return [User(**user) for user in users]

@router.post("/", response_model=User)
async def create_user(user_data: UserCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "администратор":
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Проверяем, нет ли пользователя с таким email
    cursor.execute("SELECT id FROM users WHERE email = %s", (user_data.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    
    cursor.execute("""
        INSERT INTO users (name, email, password, role) 
        VALUES (%s, %s, %s, %s) 
        RETURNING id, name, email, role
    """, (user_data.name, user_data.email, hash_password(user_data.password), user_data.role))
    
    new_user = cursor.fetchone()
    conn.commit()
    return User(**new_user)