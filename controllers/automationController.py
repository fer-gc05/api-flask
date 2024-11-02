from datetime import datetime, timedelta
from models.automationModel import AutomationModel

automation_model = AutomationModel()


class AutomationController:

    @staticmethod
    def activate_automation():
        try:
            result = automation_model.update_automation_status(1)
            return {"message": "Automatización activada"}
        except Exception as ex:
            raise Exception(f"Error activando la automatización: {str(ex)}")

    @staticmethod
    def deactivate_automation():
        try:
            result = automation_model.update_automation_status(0)
            return {"message": "Automatización desactivada"}
        except Exception as ex:
            raise Exception(f"Error desactivando la automatización: {str(ex)}")

    @staticmethod
    def update_automation_configuration(turn_on_hour: str, turn_off_hour: str):
        try:
            result = automation_model.update_automation_configuration(
                turn_on_hour, turn_off_hour
            )
            return result
        except Exception as ex:
            raise Exception(
                f"Error actualizando la configuración de automatización: {str(ex)}"
            )

    @staticmethod
    def get_automation_status():
        try:
            result = automation_model.get_automation_status()
            return result
        except Exception as ex:
            raise Exception(f"Error obteniendo el estado de automatización: {str(ex)}")

    @staticmethod
    def check_automation():
        try:
            data = automation_model.get_automation_and_device_status()
            if "message" in data:
                raise Exception(f"Error: {data['message']}")

            status = data.get("automation_status")
            turn_on_hour = data.get("turnOnHour")
            turn_off_hour = data.get("turnOffHour")
            current_time = datetime.now().strftime("%H:%M")
            current_device_status = data.get("device_status")

            turn_on_hour = AutomationController.format_time(turn_on_hour)
            turn_off_hour = AutomationController.format_time(turn_off_hour)

            if status == 1:
                if turn_on_hour <= current_time < turn_off_hour:
                    if current_device_status == 0:
                        print("Automation: Alarm activated.")
                        AutomationController.update_device_status(
                            current_device_status, 1, "Alarma activada por automatización"
                        )
                        return {"Automation": "Alarm activated."}

                elif current_time >= turn_off_hour:
                    if current_device_status == 1:
                        print("Automation: Alarm deactivated.")
                        automation_model.update_automation_status(0)
                        AutomationController.update_device_status(
                            current_device_status, 0, "Alarma desactivada por automatización"
                        )
                        return {"Automation": "Alarm deactivated."}

            return {"Automation": "No changes on automation"}
        except Exception as ex:
            raise Exception(f"Error verificando la automatización: {str(ex)}")

    @staticmethod
    def format_time(value):
            if isinstance(value, str):
                try:
                    return datetime.strptime(value, "%H:%M").strftime("%H:%M")
                except ValueError:
                    print(f"Error formateando la hora: {value}")
                    return "Formato de hora inválido"
            elif isinstance(value, timedelta):
                total_seconds = int(value.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                return f"{hours:02}:{minutes:02}"  
            return "No se ha establecido una hora"


    @staticmethod
    def update_device_status(
        current_device_status: int, new_status: int, log_message: str
    ):
        try:
            
            if current_device_status != new_status:
                result = automation_model.update_device_status(1, new_status)
                
                if result:
                    automation_model.log_alarm_action(1, log_message)
                else:
                    raise Exception("Error actualizando el estado del dispositivo")
            else:
                return {"message": "El estado del dispositivo no ha cambiado"}
        except Exception as ex:
            raise Exception(f"Error actualizando el estado del dispositivo: {str(ex)}")
