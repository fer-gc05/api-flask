from typing import Optional, List, Dict, Any
from config.database import get_connection
import pymysql

class LogsModel:
    def __init__(self):
        self.conn = get_connection()
        self.conn.autocommit(True)  

    def __del__(self):
        if self.conn.open:  
            self.conn.close()

    def get_alarm_logs(self, start_time: Optional[str] = None, end_time: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM alarm_logs WHERE 1"
        params = []
        
        if start_time and end_time:
            query += " AND DATE(timestamp) BETWEEN %s AND %s"
            params.extend([start_time, end_time])
        elif start_time:
            query += " AND DATE(timestamp) >= %s"
            params.append(start_time)
        elif end_time:
            query += " AND DATE(timestamp) <= %s"
            params.append(end_time)

        if search:
            query += " AND action LIKE %s"
            params.append(f"%{search}%")
        
        query += " ORDER BY timestamp DESC"
        
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            error_message = f"Error executing query: {e}"
            print(error_message)
            return {'error': error_message}

    def get_detection_logs(self, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM detection_logs WHERE 1"
        params = []
        
        if start_time and end_time:
            query += " AND DATE(timestamp) BETWEEN %s AND %s"
            params.extend([start_time, end_time])
        elif start_time:
            query += " AND DATE(timestamp) >= %s"
            params.append(start_time)
        elif end_time:
            query += " AND DATE(timestamp) <= %s"
            params.append(end_time)
        
        query += " ORDER BY timestamp DESC"
        
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            error_message = f"Error executing query: {e}"
            print(error_message)
            return {'error': error_message}
