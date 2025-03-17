import json
import re
from .list_files import list_files_in_directory
import requests
GEMINI_ENDPOINT = "https://maho.youapi.ir/generate"


def read_directory_path():
    config_file_path = "config.txt"
    try:
        with open(config_file_path, 'r') as file:
            directory_path = file.readline().strip()
            return directory_path
    except Exception as e:
        print(f"خطا در خواندن مسیر از فایل: {str(e)}")
        return None

def write_directory_path(new_path):
    config_file_path = "config.txt"
    try:
        with open(config_file_path, 'w') as file:
            file.write(new_path.strip())
        return True
    except Exception as e:
        print(f"خطا در نوشتن مسیر در فایل: {str(e)}")
        return False




def fix_and_parse_json(response_data):
    if isinstance(response_data, dict):
        return response_data
    pattern = re.compile(r"```json(.*?)```", re.DOTALL)
    match = pattern.search(response_data)
    if match:
        json_text = match.group(1).strip()
    else:
        pattern2 = re.compile(r"```(.*?)```", re.DOTALL)
        match2 = pattern2.search(response_data)
        if match2:
            json_text = match2.group(1).strip()
        else:
            json_text = response_data.strip()
    json_text = re.sub(r',\s*([\}\]])', r'\1', json_text)
    if not json_text:
        raise ValueError("متن پاکسازی شده خالی است.")
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        error_index = e.pos
        start_index = max(0, error_index - 50)
        end_index = error_index + 50
        snippet = json_text[start_index:end_index]
        debug_message = (
            f"خطا در تبدیل رشته به JSON: {e}\n"
            f"مشکل در نزدیکی موقعیت {error_index} در متن:\n{snippet}\n\n"
            f"متن کامل:\n{json_text}"
        )
        print(debug_message)
        raise ValueError(debug_message)

def payload (user_text: object)  -> object:
    json_list, json_info = list_files_in_directory(read_directory_path())
    text_ListDirectory = json.dumps(json_list)

    json_format = [{
        "type": "",
        "start_number_line": 0,
        "code": "",
        "Total_lines": 0,
        "end_number_line": 1,
        "new_code": ""}]

    json_format2 = [{"path": "",
                     "edits": json_format,
                     "info": "",
                     "log": ""}]

    json_formatMain = {"message": "",
                       "pip": "",
                       "edits": json_format2,
                       "log": ""}

    dastor = f"""
       میخوام با توجه به دایرکتوری فایل ها و محتوای فایل کد ها  تغییرات درخواستی رو به فرمت جیسونی که اراعه شد به من بدهی
       راهنمایی برای پر کردن مقادیر جیسون :
        -----------------------
       {json_format}
        -----------------------
       type: 
        این نوع تغییرات است و می تواند فقظ مقدار ویرایش داشته باشد
        Total_lines:
        تعداد خطوط کد  فایل اصلی داده شده 
        start_number_line:
        مقدار code از Line چند است 
        end_number_line: 
        مقدار code تا Line چند است 
        code:
        کد اصلی
        new_code:
        کد جدیدی که باید بجای کد قبلی در خطوط گفته شده قرار گیرد
        کد کامل و بدون باگ باشد
        کد ساختار درستی داشته باشد مثلا ایمپورت ها ابتدای کد قرار گیرد
        کد عملکرد خواسته شده انجام دهد
         باید محدوده ها و کپسوله هارو در نظر بگیری تا با ویرایش کد code از به new_code سینتکس کد خراب نشه
        -----------------------
        {json_format2}
        -----------------------
        path:
        مسیر فایلی که این تغییرات باید اعمال شود
        edits:
         لیستی از تغییرات مورد نیاز در کد
         دستور : نیازی به آیتم های بدون تغییر نیست و آیتم های بدون تغییر از لیست حذف کن
        log:
        توضیحاتی درمورد تغییرات
        info:
        توضیحاتی درمورد فایل
        ارتباطش با سایر فایل ها
        نحوه عملکردش
        درست بودن سینتکسش
        اگه باگی داره بگی
        -----------------------
        {json_formatMain}
        -----------------------
        message:
        توضیحات لازم به کاربر
        تمامی راهنمایی های مورد نیاز
        اگه کاربر سوالی کرده بود جوابش دقیق و کامل میدی
        edits:
        لیست تغییرات در فایل های مورد نیاز
        log:
        گزارش کاملی از شرح تغییرات لازم و نحوه استفاده
        pip:
       اگه تغییرات کتابخونه ای نیاز داره باید اینجا بگی
       اگه کاریر ازت کتابخونه ای خواست بهش میدی
       نمونه اشتباه : pip install -r requirements.txt
       نمونه صحیح: pip install requests ,flask 
        -----------------------
       """

    payload = {
        "contents": [
            {"role": "user",
             "parts": json.loads(json_info)
             },
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""Just create the outputs in the following JSON format:
                           {json_formatMain}
                           This json will be used for changes to the programming files and must be filled in carefully.
                        No changes should be made to the above Jason structure.
                           """
                    },
                    {
                        "text": f"""اسمت دستیار هوشمند ماهو است
                        برای مدیریت و تغییرات در پروژه های برنامه نویسی آفریده شدی
                        خیلی کامل هستی و دارای درو و تفکر و میتونی به درخواست های کاربر جواب کامل بدی
                        سازندت محمدجواد مختاری هست
                        وظیفته تمامی درخواست های کاربر را با دقت انجام بدی
                           """
                    },
                    {
                        "text": """
                        توانایی هات :
                        1- تغیرات دقیق و بدون نقص در کد
                        2- تحلیل کد ها و بهینه سازی
                        3- پیاده سازی قابلیت های جدید
                        4- پیشنهاد قابلیت های جدید در کد
                        5-اصلاح نام توابع و متغییر های بدون مفهوم به نام های استاندارد
                        6- پاک سازی کامند های اضافی در کد و کامند گزاری دقیق تر و بهتر
                        """
                    },
                    {
                        "text": "در ادامه لیست دایرکتوری فایل کد ها فرستاده می شود"
                    },
                    {
                        "text": text_ListDirectory
                    },
                    {
                        "text": "نکته :امکان افزودن دایرکتوری جدید برای ایجاد یک کد ماژولار را داری و میتوانی دایرکتوری های جدیدی از خودت اضاف کنی"
                    },
                    {
                        "text": dastor
                    }
                ]
            },

            {"role": "user",
             "parts": [
                 {"text": user_text}
             ]
             }]
    }
    try:
        response = requests.post(GEMINI_ENDPOINT, json=payload)
        response.raise_for_status()
        gemini_response = response.json()
        generated_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
        generated_js = fix_and_parse_json(generated_text)
        return generated_js
    except Exception as e:
        return {'error': str(e)}