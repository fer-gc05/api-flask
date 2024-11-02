from typing import Dict, Any, Optional
from config.database import get_connection
import pymysql

class AlarmModel:
    def __init__(self):
        self.conn = get_connection()
        self.conn.autocommit(True)  

    def __del__(self):
        if self.conn.open:  
            self.conn.close()

    def get_alarm_status(self, alarm_id: int) -> Dict[str, Any]:
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT status FROM devices WHERE id = %s"
                cursor.execute(sql, (alarm_id,))
                result = cursor.fetchone()
                if result:
                    return {
                        'status': 'Alarm activated' if result['status'] == 1 else 'Alarm deactivated'
                    }
                else:
                    return {'error': 'No data found'}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {'error': str(e)}

    def password_activation(self) -> Dict[str, Any]:
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT activationPassword FROM devices WHERE id = 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    return {
                        'activationPassword': result['activationPassword']
                    }
                else:
                    return {'error': 'No data found'}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {'error': str(e)}

    def update_alarm_status(self, alarm_id: int, status: int) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE devices SET status = %s WHERE id = %s"
                cursor.execute(sql, (status, alarm_id))
                return {'success': True}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {'error': str(e)}

    def insert_detection_log(self, alarm_id: int, action: str) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO detection_logs (alarm_id, action, timestamp) VALUES (%s, %s, NOW())"
                cursor.execute(sql, (alarm_id, action))
                return {'success': True}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {'error': str(e)}

    def insert_alarm_log(self, alarm_id: int, action: str) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO alarm_logs (alarm_id, action) VALUES (%s, %s)"
                cursor.execute(sql, (alarm_id, action))
                return {'success': True}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {'error': str(e)}

    def get_device_by_rfid(self, rfid: str) -> Optional[Dict[str, Any]]:
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT d.id AS device_id, d.name AS device_name, r.rfid_code, d.status, u.id AS user_id, u.username
                FROM rfid r
                INNER JOIN devices d ON r.device_id = d.id
                LEFT JOIN users u ON r.user_id = u.id
                WHERE r.rfid_code = %s
                """
                cursor.execute(sql, (rfid,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return None
        
    def get_automation_status(self, alarm_id: int) -> Dict[str, Any]:
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT status FROM automation WHERE alarm_id = %s"
                cursor.execute(sql, (alarm_id,))
                result = cursor.fetchone()
                if result:
                    return {'status': result['status']}
                else:
                    return {'error': 'No automation status found'}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {'error': str(e)}

    def update_automation_status(self, alarm_id: int, status: int) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE automation SET status = %s WHERE alarm_id = %s"
                cursor.execute(sql, (status, alarm_id))
                return {'success': True}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {'error': str(e)}