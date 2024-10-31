from typing import Dict, Any
from config.database import get_connection
import pymysql

class DeviceModel:
    def __init__(self):
        self.conn = get_connection()
        self.conn.autocommit(True)  

    def __del__(self):
        if self.conn.open:  
            self.conn.close()

    def get_device_by_id(self, device_id: int) -> Dict[str, Any]:
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM devices WHERE id = %s"
                cursor.execute(sql, (device_id,))
                result = cursor.fetchone()
                if result:
                    return result
                else:
                    return {'message': 'No device found'}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {'error': str(e)}

    def get_activation_password(self, device_id: int) -> Dict[str, Any]:
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT activationPassword FROM devices WHERE id = %s"
                cursor.execute(sql, (device_id,))
                result = cursor.fetchone()
                if result:
                    return result
                else:
                    return {'message': 'No device found'}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {'error': str(e)}

    def update_activation_password(self, device_id: int, new_password: str) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE devices SET activationPassword = %s WHERE id = %s"
                cursor.execute(sql, (new_password, device_id))
                self.conn.commit()
                return {'message': 'Password updated successfully'}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            self.conn.rollback()  
            return {'error': str(e)}
