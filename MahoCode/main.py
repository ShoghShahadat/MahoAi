from mahoBody import payload, read_directory_path,write_directory_path ,process_json
from flask import Flask, request, jsonify, render_template
import os
import json
import webbrowser
import subprocess
import tkinter as tk
from tkinter import filedialog
from mahoBody.set_json import restore_backup
import glob
app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates'
)

payloadJson = {}
libeary = ""
current_path = read_directory_path()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def handle_request():
    global payloadJson
    user_text = request.json.get('text')
    if not user_text:
        return jsonify({'error': 'متن ورودی یافت نشد'}), 400
    payloadJson = payload(user_text)
    return jsonify(payloadJson)

@app.route('/pip', methods=['GET'])
def cmd():
    global libeary, current_path
    if 'pip' in payloadJson:
        libeary = payloadJson['pip']
        try:
            os.chdir(current_path)
            command = f"start cmd /k {libeary}"
            subprocess.Popen(command, shell=True)
            return jsonify({'status': 'success', 'message': 'پنجره CMD باز شد و دستور در حال اجراست.'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'مقدار pip یافت نشد'}), 400

@app.route('/path', methods=['GET'])
def get_path():
    global current_path
    try:
        return jsonify({'path': current_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/set_json', methods=['POST'])
def set_json():
    global payloadJson
    try:
        process_json(payloadJson)
        return jsonify({'status': 'success', 'message': 'درخواست اعمال تغییرات دریافت شد.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/set_path', methods=['GET'])
def set_path():
    global current_path
    try:
        root = tk.Tk()
        root.withdraw()  # مخفی کردن پنجره اصلی
        selected_directory = filedialog.askdirectory(title="یک پوشه را انتخاب کنید")
        root.destroy()
        if selected_directory:
            current_path = selected_directory
            write_directory_path(current_path)
            return jsonify({'status': 'success', 'path': current_path})
        else:
            return jsonify({'error': 'هیچ مسیری انتخاب نشد'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/list_versions', methods=['GET'])
def list_versions():
    backup_dir = os.path.join(read_directory_path(), 'backups')
    versions = []
    if os.path.exists(backup_dir):
        version_dirs = glob.glob(os.path.join(backup_dir, 'version_*'))
        versions = [os.path.basename(version_dir).split('_')[1] for version_dir in version_dirs]
    return jsonify({'versions': versions})

@app.route('/restore_version/<version>', methods=['POST'])
def restore_version(version):
    try:
        version_number = int(version)
        if restore_backup(version_number):
            return jsonify({'status': 'success', 'message': f'Version {version} restored successfully.'})
        else:
            return jsonify({'status': 'error', 'message': f'Failed to restore version {version}.'}) , 400
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid version number.'}), 400

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:8283")
    app.run(debug=False, host='0.0.0.0', port=8283)
