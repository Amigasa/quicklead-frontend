import psycopg2
from psycopg2 import Error
from psycopg2 import extras
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
                host="localhost",
                database="progect",
                user="postgres",
                password="9365"
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
                    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'operator', 'client'))
                )
            """)

            # Таблица проектов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    api_key VARCHAR(255) UNIQUE NOT NULL,
                    applications_count INTEGER
                )
            """)

            # Таблица заявок
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id SERIAL PRIMARY KEY,
                    client_name VARCHAR(255) NOT NULL,
                    phone VARCHAR(255),
                    project_id INTEGER REFERENCES projects(id),
                    status VARCHAR(50) DEFAULT 'new' CHECK (status IN ('new', 'in_work', 'callback', 'success', 'failure')),
                    application_date DATE
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
            cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute("SELECT id, name, email, role FROM users ORDER BY id DESC")
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
    def add_project(self, name, api_key, applications_count=None):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO projects (name, api_key, applications_count)
            VALUES (%s, %s, %s)
            RETURNING id
            """
            cursor.execute(query, (name, api_key, applications_count))
            project_id = cursor.fetchone()[0]
            self.connection.commit()
            print(f"Проект '{name}' добавлен")
            return project_id
        except Error as e:
            print(f"Ошибка добавления проекта: {e}")
            return None

    def get_projects(self):
        try:
            cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute("""
                SELECT p.*, COUNT(a.id) as applications_count
                FROM projects p
                LEFT JOIN applications a ON p.id = a.project_id
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
    def add_application(self, client_name, phone=None, project_id=None):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO applications (client_name, phone, project_id)
            VALUES (%s, %s, %s)
            RETURNING id
            """
            cursor.execute(query, (client_name, phone, project_id))
            application_id = cursor.fetchone()[0]

            self.connection.commit()
            print(f"Заявка '{client_name}' добавлена")
            return application_id
        except Error as e:
            print(f"Ошибка добавления заявки: {e}")
            return None

    def get_applications(self, limit=None, offset=None):
        try:
            cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)
            query = """
                SELECT a.*, p.name as project_name
                FROM applications a
                LEFT JOIN projects p ON a.project_id = p.id
                ORDER BY a.id DESC
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

    def update_application(self, application_id, **kwargs):
        try:
            cursor = self.connection.cursor()
            updates = []
            values = []

            for key, value in kwargs.items():
                if key in ['client_name', 'phone', 'project_id', 'status']:
                    updates.append(f"{key} = %s")
                    values.append(value)

            if not updates:
                return False

            query = f"UPDATE applications SET {', '.join(updates)} WHERE id = %s"
            values.append(application_id)
            cursor.execute(query, values)

            self.connection.commit()
            print(f"Заявка ID {application_id} обновлена")
            return True
        except Error as e:
            print(f"Ошибка обновления заявки: {e}")
            return False

    def delete_application(self, application_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM applications WHERE id = %s", (application_id,))
            self.connection.commit()
            print(f"Заявка ID {application_id} удалена")
            return True
        except Error as e:
            print(f"Ошибка удаления заявки: {e}")
            return False

    def search_applications(self, search_term):
        try:
            cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)
            query = """
                SELECT a.*, p.name as project_name
                FROM applications a
                LEFT JOIN projects p ON a.project_id = p.id
                WHERE a.client_name ILIKE %s OR a.phone ILIKE %s
                ORDER BY a.id DESC
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            results = cursor.fetchall()
            print(f"Найдено заявок: {len(results)}")
            return [dict(row) for row in results]
        except Error as e:
            print(f"Ошибка поиска заявок: {e}")
            return []

    def filter_applications(self, project_id=None, status=None, date_from=None, date_to=None):
        try:
            cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)
            query = """
                SELECT a.*, p.name as project_name
                FROM applications a
                LEFT JOIN projects p ON a.project_id = p.id
                WHERE 1=1
            """
            values = []

            if project_id:
                query += " AND a.project_id = %s"
                values.append(project_id)

            if status:
                query += " AND a.status = %s"
                values.append(status)

            if date_from:
                query += " AND a.application_date >= %s"
                values.append(date_from)

            if date_to:
                query += " AND a.application_date <= %s"
                values.append(date_to)

            query += " ORDER BY a.id DESC"

            cursor.execute(query, values)
            results = cursor.fetchall()
            print(f"Найдено заявок: {len(results)}")
            return [dict(row) for row in results]
        except Error as e:
            print(f"Ошибка фильтрации заявок: {e}")
            return []

    def get_applications_not_success(self):
        try:
            cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute("""
                SELECT a.*, p.name as project_name
                FROM applications a
                LEFT JOIN projects p ON a.project_id = p.id
                WHERE a.status != 'success'
                ORDER BY a.id DESC
            """)
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except Error as e:
            print(f"Ошибка получения заявок не успешных: {e}")
            return []

    def get_stats(self):
        try:
            cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)

            # Общая статистика
            cursor.execute("""
                SELECT
                    COUNT(*) as total_applications,
                    COUNT(CASE WHEN status = 'new' THEN 1 END) as new_applications,
                    COUNT(CASE WHEN status = 'in_work' THEN 1 END) as in_work_applications,
                    COUNT(CASE WHEN status = 'success' THEN 1 END) as success_applications,
                    COUNT(CASE WHEN application_date >= CURRENT_DATE - INTERVAL '7 days' THEN 1 END) as applications_last_7_days
                FROM applications
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

    def export_applications_csv(self, filename):
        """Экспорт заявок в CSV"""
        try:
            cursor = self.connection.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute("""
                SELECT a.id, a.client_name, a.phone, p.name as project,
                       a.status, a.application_date
                FROM applications a
                LEFT JOIN projects p ON a.project_id = p.id
                ORDER BY a.id DESC
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
            applications = []

            for app in applications:
                aid = self.add_application(*app)
                if aid:
                    # Обновляем статусы для некоторых заявок
                    if aid % 2 == 0:
                        self.update_application(aid, status='in_work')
                    elif aid % 3 == 0:
                        self.update_application(aid, status='success')

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
        database="progect",
        user="postgres",
        password="9365"
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
        applications = db.get_applications(limit=5)
        print(f"\nПоследние {len(applications)} заявок:")
        for app in applications:
            print(f"  ID {app['id']}: {app['client_name']} - {app['status']}")

        # Поиск заявок
        search_results = db.search_applications("Иван")
        print(f"\nНайдено по поиску 'Иван': {len(search_results)}")

        # Фильтрация заявок
        filtered = db.filter_applications(status='new')
        print(f"Новых заявок: {len(filtered)}")

        # Экспорт в CSV
        db.export_applications_csv("leads_export.csv")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.close_connection()

if __name__ == "__main__":
    main()
