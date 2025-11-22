from fastapi import APIRouter, Depends, HTTPException, Query
from database import db
from models import Application, ApplicationCreate, User
from routers.auth import get_current_user
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("/", response_model=list[Application])
async def get_applications(
    current_user: User = Depends(get_current_user),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    project_id: Optional[int] = None,
    status: Optional[str] = None
):
    conn = db.get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT a.*, p.name as project_name
        FROM applications a
        LEFT JOIN projects p ON a.project_id = p.id
        WHERE 1=1
    """
    params = []
    
    if project_id:
        query += " AND a.project_id = %s"
        params.append(project_id)
    
    if status:
        query += " AND a.status = %s"
        params.append(status)
    
    query += " ORDER BY a.id DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    applications = cursor.fetchall()
    
    return [Application(**app) for app in applications]

@router.post("/", response_model=Application)
async def create_application(application_data: ApplicationCreate, current_user: User = Depends(get_current_user)):
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Проверяем существование проекта
    cursor.execute("SELECT id FROM projects WHERE id = %s", (application_data.project_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=400, detail="Проект не найден")
    
    cursor.execute("""
        INSERT INTO applications (client_name, phone, project_id, application_date, created_at) 
        VALUES (%s, %s, %s, %s, %s) 
        RETURNING *
    """, (
        application_data.client_name, 
        application_data.phone, 
        application_data.project_id,
        datetime.now().date(),
        datetime.now()
    ))
    
    new_application = cursor.fetchone()
    
    # Получаем название проекта
    cursor.execute("SELECT name FROM projects WHERE id = %s", (application_data.project_id,))
    project = cursor.fetchone()
    new_application["project_name"] = project["name"] if project else None
    
    conn.commit()
    
    return Application(**new_application)

@router.get("/stats")
async def get_stats(current_user: User = Depends(get_current_user)):
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT
            COUNT(*) as total_applications,
            COUNT(CASE WHEN status = 'новая' THEN 1 END) as new_applications,
            COUNT(CASE WHEN status = 'в работе' THEN 1 END) as in_progress,
            COUNT(CASE WHEN status = 'успешно' THEN 1 END) as successful
        FROM applications
    """)
    
    stats = cursor.fetchone()
    return dict(stats)