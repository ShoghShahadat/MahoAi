import os
import json
import shutil
import glob
from datetime import datetime
from .func import read_directory_path

BACKUP_DIR = read_directory_path() + "/backup"
CONFIG_FILE = os.path.join(BACKUP_DIR, "config.json")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"versions": {}}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def get_next_version():
    config = load_config()
    versions = list(map(int, config["versions"].keys()))
    return str(max(versions) + 1) if versions else "1"


def create_backup(file_path, version_dir):
    """ ایجاد یک بکاپ از فایل اصلی قبل از اعمال تغییرات """
    if not os.path.exists(version_dir):
        os.makedirs(version_dir)

    base_name = os.path.basename(file_path)
    backup_path = os.path.join(version_dir, base_name)
    shutil.copy2(file_path, backup_path)
    return backup_path


def apply_edits(file_path, edits, version):
    """اعمال تغییرات بر روی فایل مشخص شده"""
    if not os.path.exists(file_path):
        print(f"خطا: فایل {file_path} یافت نشد!")
        return

    version_dir = os.path.join(BACKUP_DIR, version)
    backup_path = create_backup(file_path, version_dir)

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for edit in edits:
        start = max(0, min(edit["start_number_line"] - 1, len(lines)))
        end = min(len(lines), edit["end_number_line"])
        new_code = edit["new_code"]

        # if edit["type"] == "اضافه":
        #     lines.insert(start, new_code + "\n")
        # elif edit["type"] == "ویرایش":
        lines[start:end] = [new_code + "\n"]

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)
    print(f"تغییرات در {file_path} با موفقیت ذخیره شد.")

    return backup_path


def process_json(json_data):
    """پردازش ورودی JSON و اعمال تغییرات در فایل‌های مشخص شده"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    version = get_next_version()
    config = load_config()
    config["versions"][version] = []

    for edit in json_data["edits"]:
        file_path = edit["path"].replace("\\", "/")
        backup_path = apply_edits(file_path, edit["edits"], version)
        config["versions"][version].append({"file": file_path, "backup": backup_path})

    save_config(config)
    print(f"ویرایش در نسخه {version} ذخیره شد.")


def list_versions():
    """نمایش نسخه‌های بکاپ ذخیره‌شده"""
    config = load_config()
    return list(config["versions"].keys())


def restore_version(version):
    """بازگردانی تمام فایل‌های تغییر یافته در یک نسخه مشخص"""
    config = load_config()
    if version not in config["versions"]:
        print(f"خطا: نسخه {version} یافت نشد!")
        return False

    for entry in config["versions"][version]:
        try:
            shutil.copy2(entry["backup"], entry["file"])
            print(f"فایل {entry['file']} از نسخه {version} بازگردانی شد.")
        except Exception as e:
            print(f"خطا در بازگردانی نسخه {version}: {str(e)}")
            return False
    return True
