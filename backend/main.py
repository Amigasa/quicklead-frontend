from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import db
from routers import auth, users, projects, applications

app = FastAPI(
    title="QuickLead Manager API",
    description="API для системы управления заявками QuickLead",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(applications.router)

@app.get("/")
async def root():
    return {"message": "QuickLead Manager API работает!"}

@app.on_event("startup")
async def startup():
    # Проверяем подключение к базе при старте
    db.get_connection()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)