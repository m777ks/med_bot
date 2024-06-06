from datetime import datetime
import re
from database.database import Database


class PatientManager:
    def __init__(self):
        self.db = Database()

    def add_patient(self, name, birthdate):
        """
        Добавляет пациента в базу данных, если имя и дата рождения корректны.
        """
        if not self.validate_name(name):
            return "Имя не должно содержать специальные символы."
        if not self.validate_birthdate(birthdate):
            return "Неверный формат даты рождения или возраст больше 100 лет."
        self.db.add_patient(name, birthdate)
        return "Пациент успешно добавлен."


    def validate_name(self, name):
        """
        Проверяет, что имя содержит только буквы и пробелы.
        """
        return re.match(r'^[a-zA-Zа-яА-Я\s]+$', name) is not None


    def validate_birthdate(self, birthdate):
        """
        Проверяет, что дата рождения валидна и возраст не превышает 100 лет.
        """
        try:
            birth_date = datetime.strptime(birthdate, '%d.%m.%Y')
            age = (datetime.now() - birth_date).days // 365
            print(age)
            return -1 < age <= 100
        except ValueError:
            return False

    def get_today_patients(self):
        """
        Возвращает список пациентов, добавленных сегодня.
        """
        return self.db.get_today_patients()

    def get_weekly_patient_counts(self):
        """
        Возвращает количество пациентов за каждый день недели.
        """
        return self.db.get_weekly_patient_counts()
