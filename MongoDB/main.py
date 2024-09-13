from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError
from bson import json_util
import json

# Підключення MongoDB Atlas
MONGODB_URI = "mongodb+srv://<username>:<password>@cluster0.c3xhe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def json_print(data):
    """
    Виводить дані у форматі JSON.
    
    Args:
        data: Дані для виводу
    """
    print(json.dumps(data, ensure_ascii=False, indent=2, default=json_util.default))

def connect_to_mongodb():
    """
    Підключення до MongoDB Atlas з обробкою винятків.
    
    Returns:
        tuple: (MongoClient, Collection) або (None, None) у випадку помилки
    """
    try:
        client = MongoClient(MONGODB_URI)
        db = client.get_database("cats_database")  # Вибір бази даних
        collection = db["cats"]
        # Перевірка підключення
        client.admin.command('ismaster')
        json_print({"message": "Успішно підключено до MongoDB Atlas"})
        return client, collection
    except ConnectionFailure as e:
        json_print({"error": f"Помилка підключення до MongoDB Atlas: {str(e)}"})
    except PyMongoError as e:
        json_print({"error": f"Виникла помилка при роботі з MongoDB: {str(e)}"})
    return None, None

def create_cat(collection, name, age, features):
    """
    Створює новий запис кота в базі даних.
    
    Args:
        collection (Collection): Колекція MongoDB
        name (str): Ім'я кота
        age (int): Вік кота
        features (list): Список особливостей кота
    
    Returns:
        bool: True, якщо кіт успішно створений, False у випадку помилки
    """
    try:
        if collection.find_one({"name": name}):
            json_print({"error": f"Кіт з ім'ям {name} вже існує."})
            return False
        
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat)
        json_print({"message": f"Створено нового кота", "id": str(result.inserted_id)})
        return True
    except OperationFailure as e:
        json_print({"error": f"Помилка операції при створенні кота: {str(e)}"})
    except PyMongoError as e:
        json_print({"error": f"Загальна помилка бази даних при створенні кота: {str(e)}"})
    return False

def update_cat(collection, name, age=None, features=None):
    """
    Оновлює інформацію про кота в базі даних.
    
    Args:
        collection (Collection): Колекція MongoDB
        name (str): Ім'я кота для оновлення
        age (int, optional): Новий вік кота
        features (list, optional): Новий список особливостей кота
    
    Returns:
        bool: True, якщо інформація успішно оновлена, False у випадку помилки
    """
    try:
        update_data = {}
        if age is not None:
            update_data["age"] = age
        if features is not None:
            update_data["features"] = features
        
        if not update_data:
            json_print({"error": "Немає даних для оновлення."})
            return False
        
        result = collection.update_one({"name": name}, {"$set": update_data})
        if result.matched_count:
            if result.modified_count:
                json_print({"message": f"Оновлено інформацію про кота: {name}"})
            else:
                json_print({"message": f"Інформація про кота {name} не змінилася."})
            return True
        else:
            json_print({"error": f"Кота з ім'ям {name} не знайдено."})
            return False
    except OperationFailure as e:
        json_print({"error": f"Помилка операції при оновленні кота: {str(e)}"})
    except PyMongoError as e:
        json_print({"error": f"Загальна помилка бази даних при оновленні кота: {str(e)}"})
    return False

def read_all_cats(collection):
    """
    Виводить всі записи котів з колекції.
    
    Args:
        collection (Collection): Колекція MongoDB
    """
    try:
        cats = list(collection.find())
        json_print(cats)
    except OperationFailure as e:
        json_print({"error": f"Помилка операції при читанні всіх котів: {str(e)}"})
    except PyMongoError as e:
        json_print({"error": f"Загальна помилка бази даних при читанні всіх котів: {str(e)}"})

def read_cat_by_name(collection, name):
    """
    Виводить інформацію про кота за ім'ям.
    
    Args:
        collection (Collection): Колекція MongoDB
        name (str): Ім'я кота для пошуку
    """
    try:
        cat = collection.find_one({"name": name})
        if cat:
            json_print(cat)
        else:
            json_print({"error": f"Кота з ім'ям {name} не знайдено."})
    except OperationFailure as e:
        json_print({"error": f"Помилка операції при пошуку кота за ім'ям: {str(e)}"})
    except PyMongoError as e:
        json_print({"error": f"Загальна помилка бази даних при пошуку кота за ім'ям: {str(e)}"})

def add_cat_feature(collection, name, new_feature):
    """
    Додає нову характеристику до списку features кота за ім'ям.
    
    Args:
        collection (Collection): Колекція MongoDB
        name (str): Ім'я кота
        new_feature (str): Нова характеристика для додавання
    """
    try:
        result = collection.update_one(
            {"name": name},
            {"$addToSet": {"features": new_feature}}
        )
        if result.matched_count:
            if result.modified_count:
                json_print({"message": f"Додано нову характеристику '{new_feature}' для кота {name}"})
            else:
                json_print({"message": f"Характеристика '{new_feature}' вже існує для кота {name}"})
        else:
            json_print({"error": f"Кота з ім'ям {name} не знайдено."})
    except OperationFailure as e:
        json_print({"error": f"Помилка операції при додаванні характеристики кота: {str(e)}"})
    except PyMongoError as e:
        json_print({"error": f"Загальна помилка бази даних при додаванні характеристики кота: {str(e)}"})

def delete_cat_by_name(collection, name):
    """
    Видаляє запис кота з колекції за ім'ям.
    
    Args:
        collection (Collection): Колекція MongoDB
        name (str): Ім'я кота для видалення
    """
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            json_print({"message": f"Кота {name} видалено з бази даних."})
        else:
            json_print({"error": f"Кота з ім'ям {name} не знайдено."})
    except OperationFailure as e:
        json_print({"error": f"Помилка операції при видаленні кота: {str(e)}"})
    except PyMongoError as e:
        json_print({"error": f"Загальна помилка бази даних при видаленні кота: {str(e)}"})

def delete_all_cats(collection):
    """
    Видаляє всі записи з колекції.
    
    Args:
        collection (Collection): Колекція MongoDB
    """
    try:
        result = collection.delete_many({})
        json_print({"message": f"Видалено {result.deleted_count} записів з бази даних."})
    except OperationFailure as e:
        json_print({"error": f"Помилка операції при видаленні всіх котів: {str(e)}"})
    except PyMongoError as e:
        json_print({"error": f"Загальна помилка бази даних при видаленні всіх котів: {str(e)}"})

if __name__ == "__main__":
    client, collection = connect_to_mongodb()
    if client is not None and collection is not None:
        try:
            # Приклади використання функцій
            create_cat(collection, "Мурзик", 2, ["сірий", "любить гратися"])
            create_cat(collection, "Барсік", 3, ["рудий", "лінивий"])
            read_all_cats(collection)
            read_cat_by_name(collection, "Мурзик")
            update_cat(collection, "Мурзик", age=3)
            add_cat_feature(collection, "Мурзик", "муркотливий")
            read_cat_by_name(collection, "Мурзик")  # Перевіряємо оновлення
            delete_cat_by_name(collection, "Барсік")
            read_all_cats(collection)  # Перевіряємо, що Барсіка видалено
            # delete_all_cats(collection)  # Будьте обережні з цією функцією!
        except PyMongoError as e:
            json_print({"error": f"Виникла неочікувана помилка при роботі з базою даних: {str(e)}"})
        finally:
            client.close()
            json_print({"message": "З'єднання з базою даних закрито"})
    else:
        json_print({"error": "Не вдалося підключитися до бази даних. Програма завершується."})
