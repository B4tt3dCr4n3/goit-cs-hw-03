import psycopg2

# Параметри підключення до бази даних
db_params = {
    "dbname": "task_management",
    "user": "postgres",
    "password": "password",
    "host": "localhost"
}

def execute_query(query, params=None, fetch=True):
    try:
        # Використання контекстного менеджера для автоматичного закриття з'єднання
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                if fetch:
                    return cur.fetchall()  # Повертаємо результат запиту
                else:
                    conn.commit()
                    return cur.rowcount  # Повертаємо кількість змінених рядків
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Помилка: {error}")

def main():
    # 1. Отримати всі завдання певного користувача
    user_id = 1
    print("Завдання для користувача 1:")
    result = execute_query("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    print(result)

    # 2. Вибрати завдання за певним статусом
    print("\nЗавдання зі статусом 'new':")
    result = execute_query("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new')")
    print(result)

    # 3. Оновити статус конкретного завдання
    task_id = 1
    new_status = 'in progress'
    rows_affected = execute_query("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s", (new_status, task_id), fetch=False)
    print(f"\nОновлено статус завдання {task_id} на '{new_status}'. Змінено рядків: {rows_affected}")

    # 4. Отримати список користувачів, які не мають жодного завдання
    print("\nКористувачі без завдань:")
    result = execute_query("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")
    print(result)

    # 5. Додати нове завдання для конкретного користувача
    new_task = ('New Task', 'Description for new task', 'new', 1)
    rows_affected = execute_query("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)", new_task, fetch=False)
    print(f"\nДодано нове завдання. Змінено рядків: {rows_affected}")

    # 6. Отримати всі завдання, які ще не завершено
    print("\nНезавершені завдання:")
    result = execute_query("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')")
    print(result)

    # 7. Видалити конкретне завдання
    task_id_to_delete = 1
    rows_affected = execute_query("DELETE FROM tasks WHERE id = %s", (task_id_to_delete,), fetch=False)
    print(f"\nВидалено завдання з id {task_id_to_delete}. Змінено рядків: {rows_affected}")

    # 8. Знайти користувачів з певною електронною поштою
    email_domain = '%@example.com'
    print("\nКористувачі з email @example.com:")
    result = execute_query("SELECT * FROM users WHERE email LIKE %s", (email_domain,))
    print(result)

    # 9. Оновити ім'я користувача
    user_id = 1
    new_name = 'New Name'
    rows_affected = execute_query("UPDATE users SET fullname = %s WHERE id = %s", (new_name, user_id), fetch=False)
    print(f"\nОновлено ім'я користувача {user_id} на '{new_name}'. Змінено рядків: {rows_affected}")

    # 10. Отримати кількість завдань для кожного статусу
    print("\nКількість завдань для кожного статусу:")
    result = execute_query("SELECT s.name, COUNT(t.id) FROM status s LEFT JOIN tasks t ON s.id = t.status_id GROUP BY s.name")
    print(result)

    # 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
    email_domain = '%@example.com'
    print("\nЗавдання для користувачів з email @example.com:")
    result = execute_query("SELECT t.* FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE %s", (email_domain,))
    print(result)

    # 12. Отримати список завдань, що не мають опису
    print("\nЗавдання без опису:")
    result = execute_query("SELECT * FROM tasks WHERE description IS NULL OR description = ''")
    print(result)

    # 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
    print("\nКористувачі та їхні завдання у статусі 'in progress':")
    result = execute_query("SELECT u.fullname, t.title FROM users u INNER JOIN tasks t ON u.id = t.user_id INNER JOIN status s ON t.status_id = s.id WHERE s.name = 'in progress'")
    print(result)

    # 14. Отримати користувачів та кількість їхніх завдань
    print("\nКористувачі та кількість їхніх завдань:")
    result = execute_query("SELECT u.fullname, COUNT(t.id) as task_count FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.id, u.fullname")
    print(result)

if __name__ == "__main__":
    main()
