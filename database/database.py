import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="patients.db"):
        """
        Инициализирует подключение к базе данных и создает таблицу, если она не существует.
        """
        self.conn = sqlite3.connect(db_name)  # Подключаемся к базе данных SQLite
        self.create_table()  # Создаем таблицу для хранения пациентов, если она еще не создана

    def create_table(self):
        """
        Создает таблицу 'patients', если она не существует.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    birthdate TEXT NOT NULL,
                    date_added TEXT NOT NULL
                )
            """)  # Создаем таблицу с полями id, name, birthdate и date_added

    def add_patient(self, name, birthdate):
        """
        Добавляет нового пациента в базу данных.
        """
        date_added = datetime.now().isoformat()  # Получаем текущую дату и время в формате ISO
        with self.conn:
            self.conn.execute("INSERT INTO patients (name, birthdate, date_added) VALUES (?, ?, ?)",
                              (name, birthdate, date_added))  # Вставляем данные о пациенте в таблицу

    def get_today_patients(self):
        """
        Возвращает список пациентов, добавленных сегодня.
        """
        today = datetime.now().date().isoformat()  # Получаем текущую дату в формате ISO
        with self.conn:
            return self.conn.execute("SELECT name, birthdate FROM patients WHERE date(date_added) = ?", (today,)).fetchall()
            # Извлекаем данные о пациентах, добавленных сегодня

    def get_weekly_patient_counts(self):
        """
        Возвращает количество пациентов за каждый день недели.
        """
        with self.conn:
            result = self.conn.execute("""
                SELECT strftime('%w', date_added) as weekday, COUNT(*) 
                FROM patients 
                GROUP BY weekday
            """).fetchall()
            # Извлекаем количество пациентов за каждый день недели
        counts = {str(i): 0 for i in range(7)}  # Инициализируем словарь для хранения количества пациентов по дням недели
        for row in result:
            counts[row[0]] = row[1]  # Заполняем словарь данными из результата запроса
        return counts
