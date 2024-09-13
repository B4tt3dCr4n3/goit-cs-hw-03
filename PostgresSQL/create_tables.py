import psycopg2

# Параметри підключення до бази даних
db_params = {
    "dbname": "task_management",
    "user": "postgres",
    "password": "password",
    "host": "localhost"
}

def create_tables():
    # Список SQL-команд для створення таблиць
    commands = [
        """
        -- Створення таблиці користувачів
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,  -- Унікальний ідентифікатор користувача, автоінкремент
            fullname VARCHAR(100) NOT NULL,  -- Повне ім'я користувача
            email VARCHAR(100) UNIQUE NOT NULL  -- Унікальна електронна адреса
        )
        """,
        """
        -- Створення таблиці статусів завдань
        CREATE TABLE status (
            id SERIAL PRIMARY KEY,  -- Унікальний ідентифікатор статусу, автоінкремент
            name VARCHAR(50) UNIQUE NOT NULL  -- Унікальна назва статусу
        )
        """,
        """
        -- Створення таблиці завдань
        CREATE TABLE tasks (
            id SERIAL PRIMARY KEY,  -- Унікальний ідентифікатор завдання, автоінкремент
            title VARCHAR(100) NOT NULL,  -- Назва завдання
            description TEXT,  -- Опис завдання
            status_id INTEGER REFERENCES status(id),  -- Зовнішній ключ до таблиці статусів
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE  -- Зовнішній ключ до таблиці користувачів з каскадним видаленням
        )
        """
    ]

    conn = None
    try:
        # Встановлення з'єднання з базою даних
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        # Виконання кожної команди зі списку
        for command in commands:
            cur.execute(command)
        
        # Закриття курсора
        cur.close()
        
        # Застосування змін
        conn.commit()
        
        print("Таблиці успішно створено")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Помилка: {error}")
    finally:
        if conn is not None:
            conn.close()  # Закриття з'єднання з базою даних

if __name__ == "__main__":
    create_tables()
