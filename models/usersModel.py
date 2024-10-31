from typing import Dict, Any, List, Optional
from config.database import get_connection
import pymysql


class UserModel:
    def __init__(self):
        self.conn = get_connection()
        self.conn.autocommit(True)

    def __del__(self):
        if self.conn.open:
            self.conn.close()

    def get_user_by_username_and_password(
        self, username: str, password: str
    ) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        params = (username, password)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM users WHERE username = %s"
        params = (username,)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None

    def create_user(self, username: str, password: str) -> bool:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        params = (username, password)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return False

    def delete_user(self, user_id: int) -> bool:
        query = "DELETE FROM users WHERE id = %s"
        params = (user_id,)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return False

    def get_user_rfid(self) -> List[Dict[str, Any]]:
        query = """
        SELECT u.id AS user_id, u.username, 
        CASE WHEN r.id IS NOT NULL THEN 'Sí' ELSE 'No' END AS rfid_asociado 
        FROM users u 
        LEFT JOIN rfid r ON u.id = r.user_id
        """

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return []

    def get_user_by_rfid(self, rfid: str) -> Optional[Dict[str, Any]]:
        query = """
        SELECT u.id AS user_id, u.username, 
        CASE WHEN r.id IS NOT NULL THEN 'Sí' ELSE 'No' END AS rfid_asociado 
        FROM users u 
        LEFT JOIN rfid r ON u.id = r.user_id 
        WHERE r.rfid_code = %s
        """
        params = (rfid,)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None

    def check_rfid_assigned(self, rfid: str):
        query = """SELECT u.id, u.username
                    FROM rfid r
                    JOIN users u ON r.user_id = u.id
                    WHERE r.rfid_code = %s;"""
        params = (rfid,)
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()  
                return result  
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None 
        

    def assign_rfid_to_user(self, rfid_code: str, user_id: int, device_id: int) -> bool:
        query = "SELECT * FROM rfid WHERE rfid_code = %s AND user_id IS NOT NULL"
        params = (rfid_code,)

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()

                if result:
                    return False

                query = "SELECT * FROM rfid WHERE rfid_code = %s"
                cursor.execute(query, params)
                result = cursor.fetchone()

                if result:
                    query = "UPDATE rfid SET user_id = %s, device_id = %s WHERE rfid_code = %s"
                    params = (user_id, device_id, rfid_code)
                else:
                    query = "INSERT INTO rfid (rfid_code, user_id, device_id) VALUES (%s, %s, %s)"
                    params = (rfid_code, user_id, device_id)

                cursor.execute(query, params)
                return cursor.rowcount > 0

        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return False

    def desassign_rfid(self, user_id: int) -> bool:
        query = "UPDATE rfid SET user_id = NULL WHERE user_id = %s"
        params = (user_id,)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return False

    def set_rfid_mode(self, mode: str) -> bool:
        rfid_status = 1 if mode == "read" else (0 if mode == "register" else None)

        if rfid_status is None:
            return False

        query = "UPDATE devices SET rfid_status = %s WHERE id = 1"
        params = (rfid_status,)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return False

    def get_rfid_mode(self) -> Optional[str]:
        query = "SELECT rfid_status FROM devices WHERE id = 1"

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    status = result["rfid_status"]
                    return (
                        "read" if status == 1 else ("register" if status == 0 else None)
                    )
                return None
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None

    def save_rfid_temp(self, rfid: str) -> bool:
        if not rfid:
            return False

        query = "UPDATE devices SET rfid_temp = %s WHERE id = 1"
        params = (rfid,)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return False

    def restart_rfid_temp(self) -> bool:
        query = "UPDATE devices SET rfid_temp = NULL WHERE id = 1"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return False

    def get_rfid_temp(self) -> Optional[str]:
        query = "SELECT rfid_temp FROM devices WHERE id = 1"

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    return result["rfid_temp"]
                else:
                    return None
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None
