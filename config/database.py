import pymysql

DATABASE_CONFIG = {
    "host": "localhost",  
    "user": "root",      
    "password": "0522",     
    "database": "pas"
}

def get_connection():
    try:
        connection = pymysql.connect(**DATABASE_CONFIG)
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
