import json
import re

def fix_and_parse_json(response_data):
    """
    این تابع ورودی که ممکن است شامل توضیحات اضافی و بلوک‌های markdown باشد را بررسی کرده و بلوک JSON را استخراج می‌کند.
    اگر ورودی از قبل دیکشنری باشد، مستقیماً برمی‌گرداند.
    """
    if isinstance(response_data, dict):
        return response_data

    # تلاش برای استخراج بلوک JSON بین ```json و ```
    pattern = re.compile(r"```json(.*?)```", re.DOTALL)
    match = pattern.search(response_data)
    if match:
        json_text = match.group(1).strip()
    else:
        # اگر بلوک json یافت نشد، سعی می‌کنیم بلوک بین ``` را استخراج کنیم
        pattern2 = re.compile(r"```(.*?)```", re.DOTALL)
        match2 = pattern2.search(response_data)
        if match2:
            json_text = match2.group(1).strip()
        else:
            # در نهایت، کل متن پاکسازی شده را در نظر می‌گیریم
            json_text = response_data.strip()

    # حذف کاماهای اضافی قبل از } یا ]
    json_text = re.sub(r',\s*([\}\]])', r'\1', json_text)

    if not json_text:
        raise ValueError("متن پاکسازی شده خالی است.")

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"خطا در تبدیل رشته به JSON: {e}")