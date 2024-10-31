from models.deviceModel import DeviceModel

device_model = DeviceModel()

class DeviceController:

    @staticmethod
    def check_password(password: str) -> dict:
        try:
            device = device_model.get_device_by_id(1)
            if 'error' in device:
                return {'status': 'error', 'message': device['error']}

            if password == device.get('activationPassword'):
                return {'status': 'success', 'message': 'Password correct'}
            else:
                return {'status': 'error', 'message': 'Password incorrect'}
        except Exception as ex:
            return {'status': 'error', 'message': f"Error checking password: {str(ex)}"}

    @staticmethod
    def update_password(current_password: str, new_password: str) -> dict:
        try:
            result = device_model.get_activation_password(1)
            if 'error' in result:
                return {'status': 'error', 'message': result['error']}
            
            stored_password = result.get('activationPassword')
            if current_password == stored_password:
                update_result = device_model.update_activation_password(1, new_password)
                if 'error' in update_result:
                    return {'status': 'error', 'message': update_result['error']}
                return {'status': 'success', 'message': 'Password updated successfully'}
            else:
                return {'status': 'error', 'message': 'The current password is incorrect'}
        except Exception as ex:
            return {'status': 'error', 'message': f"Error updating password: {str(ex)}"}
