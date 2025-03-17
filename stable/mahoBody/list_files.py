import os
import json

# لیست پسوندهای فایل‌های برنامه‌نویسی
programming_extensions = [
    '.py',    # Python
    '.dart',    # Python
    '.js',    # JavaScript
    '.ts',    # TypeScript
    '.java',  # Java
    '.c',     # C
    '.cpp',   # C++
    '.cs',    # C#
    '.rb',    # Ruby
    '.php',   # PHP
    '.html',  # HTML
    '.css',   # CSS
    '.go',    # Go
    '.rs',    # Rust
    '.kt',    # Kotlin
    '.swift', # Swift
    '.m',     # Objective-C
    '.scala', # Scala
    '.pl',    # Perl
    '.r',     # R
    '.text',     # R
    '.txt',     # R
    '.sh'     # Shell script
]

def list_files_in_directory(directory):
    file_paths = []
    file_info_list = []

    for root, _, files in os.walk(directory):
        if 'backups' in root:  # Skip the 'backups' folder and its subfolders
            continue
        for file in files:
            # فیلتر کردن فایل‌ها بر اساس پسوند
            if not file.lower().endswith(tuple(programming_extensions)):
                continue

            file_path = os.path.join(root, file)
            file_paths.append(file_path)

            # خواندن محتوای فایل و محاسبه تعداد خطوط
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                lines = content.splitlines()
                line_count = len(lines)
                # افزودن شماره خط به هر خط
                numbered_content = "\n".join([f"Line {i+1}: {line}" for i, line in enumerate(lines)])
            except Exception as e:
                content = f"خطا در خواندن فایل: {str(e)}"
                numbered_content = content
                line_count = 0

            # ایجاد فرمت مورد نظر
            file_info_list.append({
                "text": f"""
                اسم فایل : {file}
                مسیر فایل: {file_path}
                تعداد خطوط: {line_count}
                شروع کد:
                {numbered_content}
                """
            })

    return json.dumps(file_paths, ensure_ascii=False, indent=4), json.dumps(file_info_list, ensure_ascii=False, indent=4)