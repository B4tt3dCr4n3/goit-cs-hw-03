import psycopg2
from faker import Faker
import random

# Параметри підключення до бази даних
db_params = {
    "dbname": "task_management",
    "user": "postgres",
    "password": "password",
    "host": "localhost"
}

fake = Faker()  # Створення екземпляру Faker для генерації випадкових даних

def seed_data():
    conn = None
    try:
        # Встановлення з'єднання з базою даних
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Додавання користувачів
        for _ in range(10):  # Створення 10 випадкових користувачів
            cur.execute(
                "INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id",
                (fake.name(), fake.email())
            )

        # Додавання статусів
        statuses = [('new',), ('in progress',), ('completed',)]
        cur.executemany("INSERT INTO status (name) VALUES (%s)", statuses)

        # Отримання всіх id користувачів
        cur.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cur.fetchall()]
        
        # Отримання всіх id статусів
        cur.execute("SELECT id FROM status")
        status_ids = [row[0] for row in cur.fetchall()]

        # Додавання завдань
        for _ in range(30):  # Створення 30 випадкових завдань
            cur.execute(
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                (
                    fake.sentence(nb_words=4),  # Генерація випадкової назви завдання
                    fake.text(max_nb_chars=200),  # Генерація випадкового опису завдання
                    random.choice(status_ids),  # Вибір випадкового статусу
                    random.choice(user_ids)  # Вибір випадкового користувача
                )
            )

        # Застосування змін
        conn.commit()
        print("Дані успішно додано")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Помилка: {error}")
    finally:
        if conn is not None:
            conn.close()  # Закриття з'єднання з базою даних

if __name__ == "__main__":
    seed_data()
