import psycopg2
from psycopg2 import Error
import json
from datetime import datetime
import subprocess
import os

class DB:
    def __init__(self, host, database,
                 user, password):
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                host=host,
                database=postgres,
                user=postgres,
                password=progect
            )
            print("Подключение к базе данных установлено")
        except Error as e:
            print(f"Ошибка подключения: {e}")

    def create_tables(self):
        """Создание таблиц базы данных"""
        try:
            cursor = self.connection.cursor()

            # Таблица пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'operator', 'client')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Таблица проектов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    api_key VARCHAR(255) UNIQUE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Таблица заявок
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leads (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone VARCHAR(50),
                    email VARCHAR(255),
                    project_id INTEGER REFERENCES projects(id),
                    title VARCHAR(255),
                    description TEXT,
                    status VARCHAR(50) DEFAULT 'new' CHECK (status IN ('new', 'in_work', 'callback', 'success', 'failure')),
                    operator_comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Таблица истории статусов заявок
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lead_status_history (
                    id SERIAL PRIMARY KEY,
                    lead_id INTEGER REFERENCES leads(id) ON DELETE CASCADE,
                    status VARCHAR(50) NOT NULL,
                    comment TEXT,
                    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.connection.commit()
            print("Таблицы созданы успешно")
            return True
        except Error as e:
            print(f"Ошибка создания таблиц: {e}")
            return False

    # Методы для пользователей
    def add_user(self, name, email, password, role):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """
            cursor.execute(query, (name, email, password, role))
            user_id = cursor.fetchone()[0]
            self.connection.commit()
            print(f"Пользователь '{name}' добавлен")
            return user_id
        except Error as e:
            print(f"Ошибка добавления пользователя: {e}")
            return None

    def get_users(self):
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT id, name, email, role, created_at FROM users ORDER BY id")
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except Error as e:
            print(f"Ошибка получения пользователей: {e}")
            return []

    def update_user(self, user_id, name=None, email=None, role=None):
        try:
            cursor = self.connection.cursor()
            updates = []
            values = []
            if name:
                updates.append("name = %s")
                values.append(name)
            if email:
                updates.append("email = %s")
                values.append(email)
            if role:
                updates.append("role = %s")
                values.append(role)

            if not updates:
                return False

            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            values.append(user_id)
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Пользователь ID {user_id} обновлен")
            return True
        except Error as e:
            print(f"Ошибка обновления пользователя: {e}")
            return False

    def delete_user(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.connection.commit()
            print(f"Пользователь ID {user_id} удален")
            return True
        except Error as e:
            print(f"Ошибка удаления пользователя: {e}")
            return False

    # Методы для проектов
    def add_project(self, name, api_key, description=None):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO projects (name, api_key, description)
            VALUES (%s, %s, %s)
            RETURNING id
            """
            cursor.execute(query, (name, api_key, description))
            project_id = cursor.fetchone()[0]
            self.connection.commit()
            print(f"Проект '{name}' добавлен")
            return project_id
        except Error as e:
            print(f"Ошибка добавления проекта: {e}")
            return None

    def get_projects(self):
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT p.*, COUNT(l.id) as leads_count
                FROM projects p
                LEFT JOIN leads l ON p.id = l.project_id
                GROUP BY p.id
                ORDER BY p.id
            """)
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except Error as e:
            print(f"Ошибка получения проектов: {e}")
            return []

    def update_project(self, project_id, name=None, api_key=None, description=None):
        try:
            cursor = self.connection.cursor()
            updates = []
            values = []
            if name:
                updates.append("name = %s")
                values.append(name)
            if api_key:
                updates.append("api_key = %s")
                values.append(api_key)
            if description is not None:
                updates.append("description = %s")
                values.append(description)

            if not updates:
                return False

            query = f"UPDATE projects SET {', '.join(updates)} WHERE id = %s"
            values.append(project_id)
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Проект ID {project_id} обновлен")
            return True
        except Error as e:
            print(f"Ошибка обновления проекта: {e}")
            return False

    def delete_project(self, project_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
            self.connection.commit()
            print(f"Проект ID {project_id} удален")
            return True
        except Error as e:
            print(f"Ошибка удаления проекта: {e}")
            return False

    # Методы для заявок
    def add_lead(self, name, phone=None, email=None, project_id=None, title=None, description=None):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO leads (name, phone, email, project_id, title, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """
            cursor.execute(query, (name, phone, email, project_id, title, description))
            lead_id = cursor.fetchone()[0]

            # Добавляем запись в историю статусов
            cursor.execute("""
                INSERT INTO lead_status_history (lead_id, status, comment)
                VALUES (%s, 'new', 'Заявка создана')
            """, (lead_id,))

            self.connection.commit()
            print(f"Заявка '{name}' добавлена")
            return lead_id
        except Error as e:
            print(f"Ошибка добавления заявки: {e}")
            return None

    def get_leads(self, limit=None, offset=None):
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = """
                SELECT l.*, p.name as project_name
                FROM leads l
                LEFT JOIN projects p ON l.project_id = p.id
                ORDER BY l.created_at DESC
            """
            if limit:
                query += f" LIMIT {limit}"
            if offset:
                query += f" OFFSET {offset}"

            cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except Error as e:
            print(f"Ошибка получения заявок: {e}")
            return []

    def update_lead(self, lead_id, **kwargs):
        try:
            cursor = self.connection.cursor()
            updates = []
            values = []
            old_status = None

            # Получаем текущий статус для истории
            if 'status' in kwargs:
                cursor.execute("SELECT status FROM leads WHERE id = %s", (lead_id,))
                result = cursor.fetchone()
                if result:
                    old_status = result[0]

            for key, value in kwargs.items():
                if key in ['name', 'phone', 'email', 'project_id', 'title', 'description', 'status', 'operator_comment']:
                    updates.append(f"{key} = %s")
                    values.append(value)

            if not updates:
                return False

            query = f"UPDATE leads SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
            values.append(lead_id)
            cursor.execute(query, values)

            # Добавляем в историю статусов если статус изменился
            if 'status' in kwargs and old_status != kwargs['status']:
                cursor.execute("""
                    INSERT INTO lead_status_history (lead_id, status, comment)
                    VALUES (%s, %s, %s)
                """, (lead_id, kwargs['status'], kwargs.get('operator_comment', f'Статус изменен на {kwargs["status"]}')))

            self.connection.commit()
            print(f"Заявка ID {lead_id} обновлена")
            return True
        except Error as e:
            print(f"Ошибка обновления заявки: {e}")
            return False

    def delete_lead(self, lead_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM leads WHERE id = %s", (lead_id,))
            self.connection.commit()
            print(f"Заявка ID {lead_id} удалена")
            return True
        except Error as e:
            print(f"Ошибка удаления заявки: {e}")
            return False

    def search_leads(self, search_term):
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = """
                SELECT l.*, p.name as project_name
                FROM leads l
                LEFT JOIN projects p ON l.project_id = p.id
                WHERE l.name ILIKE %s OR l.phone ILIKE %s OR l.email ILIKE %s OR l.title ILIKE %s
                ORDER BY l.created_at DESC
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            results = cursor.fetchall()
            print(f"Найдено заявок: {len(results)}")
            return [dict(row) for row in results]
        except Error as e:
            print(f"Ошибка поиска заявок: {e}")
            return []

    def filter_leads(self, project_id=None, status=None, date_from=None, date_to=None):
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = """
                SELECT l.*, p.name as project_name
                FROM leads l
                LEFT JOIN projects p ON l.project_id = p.id
                WHERE 1=1
            """
            values = []

            if project_id:
                query += " AND l.project_id = %s"
                values.append(project_id)

            if status:
                query += " AND l.status = %s"
                values.append(status)

            if date_from:
                query += " AND l.created_at >= %s"
                values.append(date_from)

            if date_to:
                query += " AND l.created_at <= %s"
                values.append(date_to)

            query += " ORDER BY l.created_at DESC"

            cursor.execute(query, values)
            results = cursor.fetchall()
            print(f"Найдено заявок: {len(results)}")
            return [dict(row) for row in results]
        except Error as e:
            print(f"Ошибка фильтрации заявок: {e}")
            return []

    def get_lead_status_history(self, lead_id):
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT * FROM lead_status_history
                WHERE lead_id = %s
                ORDER BY changed_at ASC
            """, (lead_id,))
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except Error as e:
            print(f"Ошибка получения истории статусов: {e}")
            return []

    def get_stats(self):
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Общая статистика
            cursor.execute("""
                SELECT
                    COUNT(*) as total_leads,
                    COUNT(CASE WHEN status = 'new' THEN 1 END) as new_leads,
                    COUNT(CASE WHEN status = 'in_work' THEN 1 END) as in_work_leads,
                    COUNT(CASE WHEN status = 'success' THEN 1 END) as success_leads,
                    COUNT(CASE WHEN created_at >= CURRENT_DATE - INTERVAL '7 days' THEN 1 END) as leads_last_7_days
                FROM leads
            """)
            stats = dict(cursor.fetchone())
            return stats
        except Error as e:
            print(f"Ошибка получения статистики: {e}")
            return {}
            
    def export_data(self, host, user, password, db, file):
        try:
            # Используем pg_dump для PostgreSQL
            cmd = f"pg_dump -h {host} -U {user} -d {db} -f {file}"
            env = os.environ.copy()
            env['PGPASSWORD'] = password

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
            if result.returncode == 0:
                print(f"Экспорт успешен: {file}")
                return True
            else:
                print(f"Ошибка экспорта: {result.stderr}")
                return False
        except Exception as e:
            print(f"Ошибка экспорта файла: {e}")
            return False

    def import_data(self, host, user, password, db, file):
        try:
            if not os.path.exists(file):
                print(f"Файл не найден: {file}")
                return False

            # Используем psql для PostgreSQL
            cmd = f"psql -h {host} -U {user} -d {db} -f {file}"
            env = os.environ.copy()
            env['PGPASSWORD'] = password

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
            if result.returncode == 0:
                print(f"Импорт успешен: {file}")
                return True
            else:
                print(f"Ошибка импорта: {result.stderr}")
                return False
        except Exception as e:
            print(f"Ошибка импорта файла: {e}")
            return False

    def export_leads_csv(self, filename):
        """Экспорт заявок в CSV"""
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT l.id, l.name, l.phone, l.email, p.name as project,
                       l.title, l.description, l.status, l.created_at, l.operator_comment
                FROM leads l
                LEFT JOIN projects p ON l.project_id = p.id
                ORDER BY l.created_at DESC
            """)
            results = cursor.fetchall()

            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if results:
                    fieldnames = results[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in results:
                        writer.writerow(dict(row))

            print(f"Экспорт в CSV успешен: {filename}")
            return True
        except Exception as e:
            print(f"Ошибка экспорта в CSV: {e}")
            return False

    def insert_sample_data(self):
        """Вставка тестовых данных"""
        try:
            # Создаем таблицы
            self.create_tables()

            # Добавляем пользователей
            users = []

            for user in users:
                self.add_user(*user)

            # Добавляем проекты
            projects = []

            project_ids = []
            for project in projects:
                pid = self.add_project(*project)
                project_ids.append(pid)

            # Добавляем заявки
            leads = []

            for lead in leads:
                lid = self.add_lead(*lead)
                if lid:
                    # Обновляем статусы для некоторых заявок
                    if lid % 2 == 0:
                        self.update_lead(lid, status='in_work', operator_comment='Заявка взята в работу')
                    elif lid % 3 == 0:
                        self.update_lead(lid, status='success', operator_comment='Услуга оказана успешно')

            print("Тестовые данные добавлены успешно")
            return True
        except Error as e:
            print(f"Ошибка добавления тестовых данных: {e}")
            return False
        
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Подключение закрыто")

def main():
    # Пример использования базы данных
    # Замените параметры подключения на свои
    db = DB(
        host="localhost",
        database="quicklead",
        user="postgres",
        password="password"
    )

    try:
        # Создаем таблицы
        db.create_tables()

        # Добавляем тестовые данные
        db.insert_sample_data()

        # Получаем статистику
        stats = db.get_stats()
        print("Статистика:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # Получаем все заявки
        leads = db.get_leads(limit=5)
        print(f"\nПоследние {len(leads)} заявок:")
        for lead in leads:
            print(f"  ID {lead['id']}: {lead['name']} - {lead['status']}")

        # Поиск заявок
        search_results = db.search_leads("Иван")
        print(f"\nНайдено по поиску 'Иван': {len(search_results)}")

        # Фильтрация заявок
        filtered = db.filter_leads(status='new')
        print(f"Новых заявок: {len(filtered)}")

        # Экспорт в CSV
        db.export_leads_csv("leads_export.csv")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.close_connection()

if __name__ == "__main__":
    main()
