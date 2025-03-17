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
       میخوام با توجه به دایرکتوری فایل ها و محتوای فایل کد ها  تغییرات درخواستی و در نظر گرفتن و حفظ کامل زبان و سینتکس و سکوپ دلیمیترها ها کد رو به فرمت جیسونی که اراعه شد به من بدهی
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
        کد جدیدی که باید با در نظر گرفتن دقیق سکوپ دلیمیترها ها بجای کد قبلی در خطوط گفته شده قرار گیرد 
        کد ساختار درستی داشته باشد مثلا ایمپورت ها ابتدای کد قرار گیرد
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
    payload = {"system_instruction": {
        "parts":
            [
                {
                    "text": f"""Just create the outputs in the following JSON format:
                                       {json_formatMain}
                                       This json will be used for changes to the programming files and must be filled in carefully.
                                    No changes should be made to the above Jason structure.
                                       """
                },
                {
                    "text": f"""
                    هویت یابی:
                    اسمت دستیار هوشمند ماهو است
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
                    "text": "نکته :امکان افزودن دایرکتوری جدید برای ایجاد یک کد ماژولار را داری و میتوانی دایرکتوری های جدیدی از خودت اضاف کنی"
                },

                {
                    "text": dastor
                },
                {
                    "text": """
                    مهم : اگه صفحه ای مشکلات سینتکسی داشت وظیفه داری ویرایش های لازم برای خطا های سینتکسی اراعه بدی
                    نکته : اگه کدی return Scaffold( این شکلی بود باید دقت کنی موقع ویرایش و دادن کد جدید return یا سکوپ دلیمیترها ها رو پاک نکنی که کد کاربر خراب شه و باید سینتکس هارو دقیق برسی کنی و برسی کنی اگه new_code با code جایگذین شه ، کد بدست اومده خطا نداشته باشه
                   باید مستندات هر زبان کامل برسی کنی تا کد اشتباه ندی و از پارامتر های منسوخ شده هم استفاده نکنی
                   درصورت نیاز می توانی کل کد به یک باره ویرایش و در 1 ویرایش کد اصلاح شده کامل بدهی
                    """
                },
                {
                    "text": "مهم : به هیچ عنوان نباید توی کدت Line 48: اینجور شماره لاین باشه و این ها فقط برای راهنمای خودت برای پیدا کردن مقادیر لاین نامبر ها یعنی start_number_line و end_number_line هستن "
                },
                {
                    "text": "به زبان فارسی جواب کاربر بگو و میتونی درمورد دستوراتی که بهت داده شده به کاربر توضیح بدی "
                },
                {
                    "text": "دستور : باید تا 1 خط قبل و بعد new_code رو به کاربر بدی درصورت وجود و توی لاین نامبر ها ام اون 2 خط اضافی در نظر بگیری"
                }
            ]},
        "contents": [
            {"role": "user",
             "parts": json.loads(json_info)
             },
            {"role": "user",
             "parts": [{
                    "text": "در ادامه لیست دایرکتوری فایل کد ها فرستاده می شود"
                },
                {
                    "text": text_ListDirectory
                },
                 {"text": user_text}
             ]
             }],
        "generationConfig": {
            "response_mime_type": "application/json",
            "stopSequences": [
                "Title"
            ],
            "temperature": 0.3131412,
            "maxOutputTokens": 120000,
            "topP":1,
            "topK": 1
        } ,"tools": [
          {
              "google_search": {}
          }
      ]}
    try:
        response = requests.post(GEMINI_ENDPOINT, json=payload)
        response.raise_for_status()
        gemini_response = response.json()
        generated_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
        generated_js = fix_and_parse_json(generated_text)
        return generated_js
    except Exception as e:
        return {'error': str(e)}