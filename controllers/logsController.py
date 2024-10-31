from models.logsModel import LogsModel
from typing import Optional, List, Dict, Any

log_model = LogsModel()

class LogsController:

    @staticmethod
    def get_alarm_logs(start_time: Optional[str] = None, end_time: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            result = log_model.get_alarm_logs(start_time, end_time, search)
            if 'error' in result:
                return {'status': 'error', 'message': result['error']}
            return {'status': 'success', 'data': result}
        except Exception as ex:
            return {'status': 'error', 'message': f"Error retrieving alarm logs: {str(ex)}"}

    @staticmethod
    def get_detection_logs(start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            result = log_model.get_detection_logs(start_time, end_time)
            if 'error' in result:
                return {'status': 'error', 'message': result['error']}
            return {'status': 'success', 'data': result}
        except Exception as ex:
            return {'status': 'error', 'message': f"Error retrieving detection logs: {str(ex)}"}
