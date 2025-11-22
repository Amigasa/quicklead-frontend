import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=DATABASE_CONFIG["host"],
                database=DATABASE_CONFIG["database"],
                user=DATABASE_CONFIG["user"],
                password=DATABASE_CONFIG["password"],
                cursor_factory=RealDictCursor
            )
            print("✅ Подключение к базе данных установлено")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")

    def get_connection(self):
        if self.connection is None or self.connection.closed:
            self.connect()
        return self.connection

db = Database()