// Создаем базу данных и настраиваем пользователей
db = db.getSiblingDB('products_db');

// Создаем пользователя для базы данных products_db
db.createUser({
    user: "app_user",
    pwd: "123",
    roles: [
    { role: "readWrite", db: "products_db" }
    ]
});


// Создаем коллекцию products если ее нет
if (!db.getCollectionNames().includes("products")) {
    db.createCollection("products");
}

print("MongoDB initialization completed!");