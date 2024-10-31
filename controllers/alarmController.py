from models.alarmModel import AlarmModel

alarm_model = AlarmModel()


class AlarmController:

    @staticmethod
    def check_status(alarm_id: int):
        try:
            result = alarm_model.get_alarm_status(alarm_id)
            return result
        except Exception as ex:
            raise Exception(f"Error checking alarm status: {str(ex)}")

    @staticmethod
    def toggle_alarm(rfid: str):
        try:
            result = alarm_model.get_device_by_rfid(rfid)

            if not result:
                raise Exception("RFID no existente")

            alarm_id = result["device_id"]
            status = alarm_model.get_alarm_status(alarm_id)
            current_status = status["status"]
            new_status = 0 if current_status == "Alarm activated" else 1

            alarm_model.update_alarm_status(alarm_id, new_status)

            message = "Alarm activated" if new_status == 1 else "Alarm deactivated"
            action = (
                f'Alarma activada por {result["username"]}'
                if new_status == 1
                else f'Alarma desactivada por {result["username"]}'
            )

            alarm_model.insert_alarm_log(alarm_id, action)

            if new_status == 0:
                AlarmController.deactivate_automation(alarm_id)

            return {"success": message}

        except Exception as ex:
            raise Exception(f"Error toggling alarm: {str(ex)}")

        

    @staticmethod
    def turn_on_alarm(password: str):
        try:
            result = alarm_model.get_alarm_status(1)

            if result["status"] == "Alarm deactivated":
                if password == result["activationPassword"]:
                    alarm_model.update_alarm_status(1, 1)
                    alarm_model.insert_alarm_log(1, "Alarma activada por interfaz web")
                    return {"message": "Alarm activated"}
                else:
                    raise Exception("Incorrect password")
            else:
                return {"message": "Alarm already activated"}

        except Exception as ex:
            raise Exception(f"Error turning on alarm: {str(ex)}")

    @staticmethod
    def turn_off_alarm(password: str):
        try:
            result = alarm_model.get_alarm_status(1)

            if result["status"] == "Alarm activated":
                if password == result["activationPassword"]:
                    alarm_model.update_alarm_status(1, 0)
                    alarm_model.insert_alarm_log(1, "Alarma desactivada por interfaz web")
                    AlarmController.deactivate_automation(1)
                    return {"message": "Alarm deactivated"}
                else:
                    raise Exception("Incorrect password")
            else:
                return {"message": "Alarm already deactivated"}

        except Exception as ex:
            raise Exception(f"Error turning off alarm: {str(ex)}")

    @staticmethod
    def intruder_detected():
        try:
            result = alarm_model.insert_detection_log(1, "Intruso detectado")
            if "success" in result:
                return {"message": "Detection log inserted"}
            else:
                raise Exception("Error inserting detection log")
        except Exception as ex:
            raise Exception(f"Error detecting intruder: {str(ex)}")

    @staticmethod
    def deactivate_automation(alarm_id: int):
        try:
            result = alarm_model.get_automation_status(alarm_id)
            if "error" in result:
                raise Exception("Error retrieving automation status")

            # Verificar si la automatización está activada y desactivarla si es necesario
            if result["status"] == 1:
                update_result = alarm_model.update_automation_status(alarm_id, 0)
                if "success" not in update_result:
                    raise Exception("Error deactivating automation")

        except Exception as ex:
            raise Exception(f"Error deactivating automation: {str(ex)}")
