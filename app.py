from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pathlib import Path
import json
from models.usersModel import UserModel
from controllers.alarmController import AlarmController
from controllers.usersController import UserController
from controllers.automationController import AutomationController
from controllers.logsController import LogsController
from controllers.deviceController import DeviceController

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

user_model = UserModel()
ALARM_STATUS_FILE = Path("alarm_status.json")

def save_alarm_status(alarm_status):
    with open(ALARM_STATUS_FILE, "w") as file:
        json.dump(alarm_status, file)

def check_alarm_status(alarm_id=1):
    try:
        result = AlarmController.check_status(alarm_id)
        save_alarm_status(result)
    except Exception as e:
        print(f"Error verificando el estado de la alarma: {str(e)}")

@app.route("/", methods=["GET"])
def index():
    return "Bienvenido a la API de la alarma"

@app.route("/login", methods=["POST"])
def login_route():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify({"error": "El nombre de usuario y la contraseña son obligatorios"}), 400

    try:
        result = UserController.login(username, password)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@app.route("/alarm/status", methods=["GET"])
def get_alarm_status():
    try:
        if not os.path.exists(ALARM_STATUS_FILE):
            return jsonify({"status": "Alarm status not available"}), 404
        with open(ALARM_STATUS_FILE, "r") as file:
            alarm_status = json.load(file)

        return jsonify(alarm_status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/alarm/toggle/<string:rfid>", methods=["POST"])
def toggle_alarm(rfid):
    try:
        result = AlarmController.toggle_alarm(rfid)
        check_alarm_status()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/alarm/turn_on", methods=["POST"])
def turn_on_alarm():
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "Password is required"}), 400
    try:
        result = AlarmController.turn_on_alarm(password)
        check_alarm_status()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/alarm/turn_off", methods=["POST"])
def turn_off_alarm():
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "Password is required"}), 400
    try:
        result = AlarmController.turn_off_alarm(password)
        check_alarm_status()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@app.route("/alarm/intruder_detected", methods=["POST"])
def intruder_detected():
    try:
        result = AlarmController.intruder_detected()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rutas de UserController
@app.route("/user/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        result = UserController.delete_user(user_id)
        return jsonify({"status": "User successfully deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/user/assign_rfid", methods=["POST"])
def assign_rfid_to_user():
    rfid_code = request.form.get("rfid_code")
    user_id = request.form.get("user_id")
    device_id = request.form.get("device_id")

    if not rfid_code or not user_id or not device_id:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        result = UserController.assign_rfid_to_user(rfid_code, int(user_id), int(device_id))
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/user/desassign_rfid/<int:user_id>", methods=["POST"])
def desassign_rfid(user_id):
    try:
        result = UserController.desassign_rfid(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/user/get_user_rfid", methods=["GET"])
def get_user_rfid():
    try:
        result = UserController.get_user_rfid()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/user/set_rfid_mode", methods=["POST"])
def set_rfid_mode():
    mode = request.form.get("mode")

    if not mode:
        return jsonify({"error": "Modo RFID es obligatorio"}), 400

    try:
        result = UserController.set_rfid_mode(mode)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/user/get_rfid_mode", methods=["GET"])
def get_rfid_mode():
    try:
        result = UserController.get_rfid_mode()
        return jsonify({"mode": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/user/save_rfid_temp", methods=["POST"])
def save_rfid_temp():
    rfid = request.form.get("rfid")
    if not rfid:
        return jsonify({"error": "El código RFID es obligatorio"}), 400

    try:
        result = UserController.save_rfid_temp(rfid)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/user/restart_rfid_temp", methods=["POST"])
def restart_rfid_temp():
    try:
        result = UserController.restart_rfid_temp()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/user/get_rfid_temp", methods=["GET"])
def get_rfid_temp():
    try:
        result = UserController.get_rfid_temp()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/user/create", methods=["POST"])
def create_user():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify({"error": "El nombre de usuario y la contraseña son obligatorios"}), 400

    try:
        result = UserController.create_user(username, password)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rutas de AutomationController
@app.route("/automation/status", methods=["GET"])
def get_automation_status():
    try:
        result = AutomationController.get_automation_status()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/automation/check", methods=["GET"])
def check_automation():
    try:
        result = AutomationController.check_automation()
        if result["Automation"] in ["Alarm activated.", "Alarm deactivated."]:
            check_alarm_status()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/automation/activate", methods=["POST"])
def activate_automation():
    try:
        result = AutomationController.activate_automation()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/automation/deactivate", methods=["POST"])
def deactivate_automation():
    try:
        result = AutomationController.deactivate_automation()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/automation/configure", methods=["POST"])
def update_automation_configuration():
    turn_on_hour = request.form.get("turn_on_hour")
    turn_off_hour = request.form.get("turn_off_hour")

    if not turn_on_hour or not turn_off_hour:
        return jsonify({"error": "Se requieren las horas de encendido y apagado"}), 400

    try:
        result = AutomationController.update_automation_configuration(turn_on_hour, turn_off_hour)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rutas de LogsController
@app.route("/logs/alarm", methods=["GET"])
def get_alarm_logs():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    search = request.args.get("search")
    result = LogsController.get_alarm_logs(start_time, end_time, search)
    return jsonify(result)

@app.route("/logs/detection", methods=["GET"])
def get_detection_logs():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    result = LogsController.get_detection_logs(start_time, end_time)
    return jsonify(result)

# Rutas de DeviceController
@app.route("/device/check-password", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password")
    if not password:
        return jsonify({"status": "error", "message": "Password is required"})

    result = DeviceController.check_password(password)
    return jsonify(result)

@app.route("/device/update-password", methods=["POST"])
def update_password():
    data = request.get_json()
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:
        return jsonify({
            "status": "error",
            "message": "Both current and new passwords are required",
        })

    result = DeviceController.update_password(current_password, new_password)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
