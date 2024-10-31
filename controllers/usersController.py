from models.usersModel import UserModel

user_model = UserModel()

class UserController:

    @staticmethod
    def delete_user(user_id: int):
        try:
            result = user_model.delete_user(user_id)
            if not result:
                raise Exception("Error al eliminar el usuario.")
            return {"status": "Usuario eliminado exitosamente."}
        except Exception as ex:
            raise Exception(f"Error en delete_user: {str(ex)}")
        
    @staticmethod
    def assign_rfid_to_user(rfid_code: str, user_id: int, device_id: int):
        try:
            if not rfid_code or not user_id or not device_id:
                raise Exception("Todos los campos son obligatorios para asignar el RFID.")
            
            existing_user = user_model.check_rfid_assigned(rfid_code)
            
            if existing_user: 
                username = existing_user[1] 
                raise Exception("RFID ya asignado.") 
            
            result = user_model.assign_rfid_to_user(rfid_code, user_id, device_id)
            if not result:
                raise Exception("Error al asignar el RFID.")
            
            return {"status": "RFID asignado exitosamente."}
        
        except Exception as ex:
            if str(ex) == "RFID ya asignado.":
                return {"error": str(ex)}
            raise Exception(f"Error en assign_rfid_to_user: {str(ex)}")


    @staticmethod
    def desassign_rfid(user_id: int):
        try:
            if not user_id:
                raise Exception("ID del usuario es obligatorio.")
            
            result = user_model.desassign_rfid(user_id)
            if not result:
                raise Exception("Error al desasignar el RFID.")
            return {"status": "success"}
        except Exception as ex:
            raise Exception(f"Error en desassign_rfid: {str(ex)}")

    @staticmethod
    def get_user_rfid():
        try:
            result = user_model.get_user_rfid()
            if not result:
                raise Exception("Error al obtener los usuarios con RFID.")
            return result
        except Exception as ex:
            raise Exception(f"Error en get_user_rfid: {str(ex)}")

    @staticmethod
    def set_rfid_mode(mode: str):
        try:
            if not mode:
                raise Exception("Modo RFID es obligatorio.")
            
            result = user_model.set_rfid_mode(mode)
            if not result:
                raise Exception("Error al establecer el modo RFID.")
            return {"status": "Modo RFID establecido correctamente."}
        except Exception as ex:
            raise Exception(f"Error en set_rfid_mode: {str(ex)}")

    @staticmethod
    def get_rfid_mode():
        try:
            result = user_model.get_rfid_mode()
            if result is None:
                raise Exception("Error al obtener el modo RFID.")
            return result
        except Exception as ex:
            raise Exception(f"Error en get_rfid_mode: {str(ex)}")

    @staticmethod
    def save_rfid_temp(rfid: str):
        try:
            if not rfid:
                raise Exception("El código RFID es obligatorio.")
            
            result = user_model.save_rfid_temp(rfid)
            if not result:
                raise Exception("Error al guardar el código RFID temporal.")
            return {"status": "Código RFID temporal guardado exitosamente."}
        except Exception as ex:
            raise Exception(f"Error en save_rfid_temp: {str(ex)}")

    @staticmethod
    def restart_rfid_temp():
        try:
            result = user_model.restart_rfid_temp()
            if not result:
                raise Exception("Error al reiniciar el código RFID temporal.")
            return {"status": "Código RFID temporal reiniciado exitosamente."}
        except Exception as ex:
            raise Exception(f"Error en restart_rfid_temp: {str(ex)}")

    @staticmethod
    def get_rfid_temp():
        try:
            result = user_model.get_rfid_temp()
            if result is None or result == "": 
                return {"rfid_temp": "", "message": "El campo RFID temporal está vacío."}
            
            return {"rfid_temp": result}
        except Exception as ex:
            raise Exception(f"Error en get_rfid_temp: {str(ex)}")


    @staticmethod
    def create_user(username: str, password: str):
        try:
            if not username or not password:
                raise Exception("El nombre de usuario y la contraseña son obligatorios.")
            
            result = user_model.create_user(username, password)
            if not result:
                raise Exception("Error al crear el usuario.")
            
            return {"status": "Usuario creado exitosamente."}
        except Exception as ex:
            raise Exception(f"Error en create_user: {str(ex)}")