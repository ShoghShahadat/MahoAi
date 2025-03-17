import os
import json
import shutil
from datetime import datetime
import configparser
from .func import read_directory_path

BACKUP_BASE_DIR = 'backups'

def getBackupDr():
    current_path = read_directory_path()
    BACKUP_DI = os.path.join(current_path, BACKUP_BASE_DIR)
    return BACKUP_DI

def get_backup_dir():
    config_file_path = 'config.txt'
    try:
        with open(config_file_path, 'r') as file:
            directory_path = file.readline().strip()
            return os.path.join(directory_path, BACKUP_BASE_DIR)
    except Exception as e:
        print(f'Error reading directory path from file: {e}')
        return BACKUP_BASE_DIR



def get_next_version_number():
    config = configparser.ConfigParser()
    config_file_path = os.path.join(getBackupDr(), 'backup_config.ini')

    if os.path.exists(config_file_path):
        config.read(config_file_path)
        last_version = config.getint('BACKUP', 'last_version', fallback=0)
        next_version = last_version + 1
    else:
        next_version = 1

    return next_version

def update_version_number(version_number):
    config = configparser.ConfigParser()
    config_file_path = os.path.join(getBackupDr(), 'backup_config.ini')

    config['BACKUP'] = {
        'last_version': str(version_number)
    }

    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

def create_backup(file_path):
    """Creates a backup of the original file before making changes"""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found!")
        return None

    if not os.path.exists(getBackupDr()):
        os.makedirs(getBackupDr())

    version_number = get_next_version_number()
    backup_dir_version = os.path.join(getBackupDr(), f'version_{version_number}')
    os.makedirs(backup_dir_version, exist_ok=True)

    # Calculate relative path
    base_dir = os.path.dirname(get_backup_dir())  # Parent of getBackupDr()
    relative_path = os.path.relpath(file_path, base_dir)
    backup_file_path = os.path.join(backup_dir_version, relative_path)

    # Create necessary subdirectories in backup
    os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)
    shutil.copy2(file_path, backup_file_path + '.bk')
    print(f'Backup created: {backup_file_path}')

    update_version_number(version_number)
    return version_number
def apply_edits(file_path, edits):
    """Apply changes to the specified file"""
    # اگر فایل وجود ندارد، آن را بساز
    if not os.path.exists(file_path):
        print(f"فایل {file_path} پیدا نشد، در حال ساخت فایل...")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # ساخت دایرکتوری‌ها اگر وجود ندارند
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")  # ساخت یک فایل خالی
        print(f"فایل {file_path} با موفقیت ساخته شد")

    # بکاپ قبل از اعمال تغییرات
    create_backup(file_path)

    # خواندن محتوای فایل (اگر خالی باشد، lines خالی خواهد بود)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # اعمال تغییرات
    for edit in edits:
        total_lines = len(lines)
        start = max(0, min(edit["start_number_line"] - 1, total_lines))  # خط شروع
        end = min(total_lines, edit["end_number_line"])  # خط پایان
        new_code = edit["new_code"]
        lines[start:end] = [new_code + "\n"]  # جایگزینی خطوط

    # نوشتن تغییرات در فایل
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

    print(f"Changes successfully saved to {file_path}")
    return True

def process_json(json_data):
    """Process JSON input and apply changes to specified files"""
    try:
        data = json.loads(json_data) if isinstance(json_data, str) else json_data

        if not isinstance(data, dict) or "edits" not in data:
            print("خطا: داده JSON باید یه دیکشنری با کلید 'edits' باشه!")
            return False

        edits_list = data["edits"]
        if not isinstance(edits_list, list):
            print("خطا: 'edits' باید یه لیست باشه!")
            return False

        if not os.path.exists(getBackupDr()):
            os.makedirs(getBackupDr())

        for edit in edits_list:
            if not isinstance(edit, dict) or "path" not in edit or "edits" not in edit:
                print("خطا: هر تغییر باید شامل 'path' و 'edits' باشه!")
                continue

            file_path = edit["path"].replace("\\", "/")
            if not isinstance(edit["edits"], list):
                print(f"خطا: 'edits' برای {file_path} باید یه لیست باشه!")
                continue

            if apply_edits(file_path, edit["edits"]):
                print(f"تغییرات با موفقیت برای {file_path} اعمال شد")
            else:
                print(f"خطا در پردازش تغییرات برای {file_path}")

        return True
    except Exception as e:
        print(f"خطا در پردازش داده JSON: {e}")
        return False

def restore_backup(version_number):
    """Restore files from a specific backup version"""
    backup_dir_version = os.path.join(getBackupDr(), f'version_{version_number}')
    if not os.path.exists(backup_dir_version):
        print(f'Error: Backup version {version_number} not found!')
        return False

    try:
        # Get the original base directory from config.txt
        config_file_path = 'config.txt'
        with open(config_file_path, 'r') as file:
            original_base_dir = file.readline().strip()

        # Walk through the backup directory
        for root, _, files in os.walk(backup_dir_version):
            for filename in files:
                backup_file_path = os.path.join(root, filename)
                # Calculate the relative path from the backup version directory
                relative_path = os.path.relpath(backup_file_path, backup_dir_version)
                # Construct the original file path
                original_file_path = os.path.join(original_base_dir, relative_path)

                # Create necessary subdirectories in the original location
                os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
                # Restore the file
                if backup_file_path.endswith('.bk'):
                    original_file_path = original_file_path[:-3]
                shutil.copy2(backup_file_path, original_file_path)
                print(f'File restored: {original_file_path}')

        return True
    except Exception as e:
        print(f'Error restoring backup: {e}')
        return False