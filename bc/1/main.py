from mahoBody import *
from flask import Flask, request, jsonify, render_template
import os
import json
import webbrowser
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

payloadJson = {}
libeary = ""
current_path = read_directory_path()
backup_dir = os.path.join(current_path, "backups")
config_path = os.path.join(backup_dir, "config.json")


def save_config(version, edited_files):
    """ ذخیره نسخه‌های بکاپ در فایل کانفیگ """
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    config[version] = edited_files
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def get_latest_version():
    """ دریافت آخرین نسخه ذخیره‌شده در فایل کانفیگ """
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return max(map(int, config.keys()), default=0)
    return 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def handle_request():
    global payloadJson, current_path
    user_text = request.json.get("text")
    if not user_text:
        return jsonify({'error': 'متن ورودی یافت نشد'}), 400
    payloadJson = payload(user_text)
    return jsonify(payloadJson)


@app.route('/pip', methods=['POST'])
def cmd():
    global libeary
    if 'pip' in payloadJson:
        libeary = payloadJson['pip']
        try:
            os.chdir(current_path)
            command = f"start cmd /k {libeary}"
            subprocess.Popen(command, shell=True)
            return jsonify({'status': 'success', 'message': 'دستور در حال اجرا است.'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'مقدار pip یافت نشد'}), 400


@app.route('/get_path', methods=['GET'])
def get_path():
    global current_path
    return jsonify({'path': current_path})


@app.route('/set_json', methods=['GET'])
def set_json():
    try:
        json_data = request.json
        process_json(json_data)
        return jsonify({'status': 'success', 'message': 'درخواست اعمال تغییرات دریافت شد.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/path', methods=['GET'])
def get_path_dr():
    global current_path
    try:
        return jsonify({'path': current_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/set_path', methods=['GET'])
def set_path():
    global current_path
    try:
        root = tk.Tk()
        root.withdraw()
        selected_directory = filedialog.askdirectory(title="یک پوشه را انتخاب کنید")
        root.destroy()
        if selected_directory:
            current_path = selected_directory
            return jsonify({'status': 'success', 'path': current_path})
        else:
            return jsonify({'error': 'هیچ مسیری انتخاب نشد'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/list_versions', methods=['GET'])
def list_versions_route():
    try:
        versions = list_versions()
        return jsonify({'versions': versions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/restore_version', methods=['POST'])
def restore_version_route():
    try:
        version = request.json.get('version')
        if not version:
            return jsonify({'error': 'شماره نسخه را مشخص کنید'}), 400

        if restore_version(version):
            return jsonify({'status': 'success', 'message': f'نسخه {version} با موفقیت بازگردانی شد.'})
        else:
            return jsonify({'error': 'خطا در بازگردانی نسخه'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:8283")
    app.run(debug=False, host='0.0.0.0', port=8283)
