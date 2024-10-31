from typing import Dict, Any
from config.database import get_connection
import pymysql
from datetime import datetime, timedelta


class AutomationModel:
    def __init__(self):
        self.conn = get_connection()
        self.conn.autocommit(True)

    def __del__(self):
        if self.conn.open:
            self.conn.close()

    def get_automation_status(self) -> Dict[str, Any]:
        def format_time(time_value):
            if time_value is None:
                return "No time set"
            if isinstance(time_value, str):
                try:
                    datetime.strptime(time_value, "%H:%M")
                    return time_value
                except ValueError:
                    return "Invalid time format"
            if isinstance(time_value, timedelta):
                return (datetime.min + time_value).time().strftime("%H:%M")
            return "Invalid time format"

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT status, turnOnHour, turnOffHour FROM automation WHERE id = 1"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    result["turnOnHour"] = format_time(result.get("turnOnHour"))
                    result["turnOffHour"] = format_time(result.get("turnOffHour"))
                    return result
                else:
                    return {"message": "No data found"}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {"error": str(e)}

    def update_automation_status(self, status: int) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE automation SET status = %s WHERE id = 1"
                cursor.execute(sql, (status,))
                return {"message": "Automation status updated"}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {"error": str(e)}

    def update_automation_configuration(
        self, turn_on_hour: str, turn_off_hour: str
    ) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE automation SET status = 1, turnOnHour = %s, turnOffHour = %s WHERE id = 1"
                cursor.execute(sql, (turn_on_hour, turn_off_hour))
                return {"message": "Configuration updated successfully"}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {"error": str(e)}

    def get_automation_and_device_status(self) -> Dict[str, Any]:
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT a.status AS automation_status, a.turnOnHour, a.turnOffHour, d.status AS device_status
                FROM automation a
                JOIN devices d ON d.id = 1
                WHERE a.id = 1
                """
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    return result
                else:
                    return {"message": "No data found"}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {"error": str(e)}

    def update_device_status(self, alarm_id: int, status: int) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE devices SET status = %s WHERE id = %s"
                cursor.execute(sql, (status, alarm_id))
                return {"message": "Device status updated"}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {"error": str(e)}

    def log_alarm_action(self, alarm_id: int, action: str) -> Dict[str, Any]:
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO alarm_logs (alarm_id, action) VALUES (%s, %s)"
                cursor.execute(sql, (alarm_id, action))
                return {"success": True}
        except pymysql.MySQLError as e:
            print(f"Database error while logging action: {e}")
            return {"error": str(e)}
