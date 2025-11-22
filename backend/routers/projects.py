from fastapi import APIRouter, Depends, HTTPException
from database import db
from models import Project, ProjectCreate, User
from routers.auth import get_current_user
import secrets
import string

router = APIRouter(prefix="/projects", tags=["projects"])

def generate_api_key():
    alphabet = string.ascii_letters + string.digits
    return "qlm_" + ''.join(secrets.choice(alphabet) for _ in range(16))

@router.get("/", response_model=list[Project])
async def get_projects(current_user: User = Depends(get_current_user)):
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, COUNT(a.id) as applications_count
        FROM projects p
        LEFT JOIN applications a ON p.id = a.project_id
        GROUP BY p.id
        ORDER BY p.id
    """)
    projects = cursor.fetchall()
    return [Project(**project) for project in projects]

@router.post("/", response_model=Project)
async def create_project(project_data: ProjectCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["администратор", "оператор"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    api_key = generate_api_key()
    
    cursor.execute("""
        INSERT INTO projects (name, api_key) 
        VALUES (%s, %s) 
        RETURNING *
    """, (project_data.name, api_key))
    
    new_project = cursor.fetchone()
    new_project["applications_count"] = 0
    conn.commit()
    return Project(**new_project)