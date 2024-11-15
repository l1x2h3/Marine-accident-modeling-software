import hashlib
import mysql.connector
from database.db_config import db_config
# 注册用户

# 创建数据库连接
def create_connection():
    return mysql.connector.connect(**db_config)

def register_user(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (email, password) VALUES (%s, %s)"
    cursor.execute(query, (email, hashed_password))
    connection.commit()
    cursor.close()
    connection.close()

# 检查用户是否存在
def check_user(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, hashed_password))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None

