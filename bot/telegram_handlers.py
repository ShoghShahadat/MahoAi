import os, asyncio
from telegram import Update, InputMediaPhoto, InputMediaDocument, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext
from image_generator import generate_image_without_removal
from promts import generate_prompts
from config import MODE_NAMES, CHANNEL_ID, mass

user_settings = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "سلام! خوبی؟ متن خود را ارسال کنید تا تصاویر مربوطه را بسازم.\n"
        "برای تغییر حالت تصویرسازی از دستور /settings استفاده کن.\n"
        "حالت پیش‌فرض: دقیق")

async def settings(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    current_mode = user_settings.get(user_id, "precise")
    keyboard = [
        [InlineKeyboardButton(f"حالت دقیق {'✅' if current_mode == 'precise' else ''}", callback_data="mode_precise")],
        [InlineKeyboardButton(f"حالت خلاقانه {'✅' if current_mode == 'creative' else ''}", callback_data="mode_creative")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"لطفاً حالت مورد نظر خود را انتخاب کنید:\nحالت فعلی: {MODE_NAMES[current_mode]}",
        reply_markup=reply_markup)

async def settings_callback(update: Update, context: CallbackContext):
    query: CallbackQuery = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == "mode_precise":
        user_settings[user_id] = "precise"
        await query.edit_message_text("حالت دقیق انتخاب شد. حالا تصاویر با دقت بالا تولید می‌شوند!")
    elif query.data == "mode_creative":
        user_settings[user_id] = "creative"
        await query.edit_message_text("حالت خلاقانه انتخاب شد. تصاویر با خلاقیت بیشتری ساخته می‌شوند!")
    else:
        await query.edit_message_text("انتخاب نامعتبر.")

async def handle_text(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_text = update.message.text.strip()
    if not user_text:
        await update.message.reply_text("لطفاً یک متن معتبر ارسال کنید.")
        return
    mode = user_settings.get(user_id, "precise")
    asyncio.create_task(process_request(update, context, mode))


async def process_request(update: Update, context: CallbackContext, mode: str):
    user_text = update.message.text
    processing_msg = await update.message.reply_text(
        f"در حال پردازش درخواست شما... 🕒\nمدل انتخاب‌شده: {MODE_NAMES[mode]}"
    )

    # تولید پرامپت‌ها
    try:
        prompts_array, prompts_caption, prompts_Advertising = await generate_prompts(user_text, mode)
    except Exception as e:
        await update.message.reply_text(f"خطا در تولید پرامپت: {str(e)}")
        return

    total = len(prompts_array)
    tasks = [process_single_image(prompt, i + 1, total, update) for i, prompt in enumerate(prompts_array)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # جمع‌آوری تصاویر موفق
    image_paths = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            await update.message.reply_text(f"خطا در پردازش تصویر {i + 1}: {str(result)}")
        elif result:  # اگر نتیجه معتبر باشد
            image_paths.append(result)

    # ارسال تصاویر به کاربر
    photos_user = []
    for path, _ in image_paths:
        if os.path.exists(path):
            photos_user.append(InputMediaPhoto(open(path, 'rb')))
    if photos_user:
        await update.message.reply_media_group(photos_user)
    await update.message.reply_text(prompts_caption)

    # ارسال به کانال در صورت لزوم
    if not prompts_Advertising:  # اگر prompts_Advertising False باشه، به کانال ارسال می‌شه
        photos_channel = []
        for path, _ in image_paths:
            if os.path.exists(path):
                photos_channel.append(InputMediaPhoto(open(path, 'rb')))
        if photos_channel:
            await context.bot.send_media_group(chat_id=CHANNEL_ID, media=photos_channel)
            await context.bot.send_message(chat_id=CHANNEL_ID, text=user_text)

    # حذف پیام پردازش
    await processing_msg.delete()

    # پاکسازی فایل‌های موقت
    for path, _ in image_paths:
        if os.path.exists(path):
            os.remove(path)

async def process_single_image(prompt, index: int, total: int, update: Update):
    max_retries = 5  # حداکثر تعداد تلاش‌ها

    for attempt in range(max_retries):
        try:
            prompt["remove"] = False  # جلوگیری از حذف پس‌زمینه
            return await generate_image_without_removal(prompt)  # ساخت تصویر
        except Exception as e:
            error_message = str(e)
            if "Capacity temporarily exceeded" in error_message:
                if attempt < max_retries - 1:  # اگر هنوز تلاش باقی مانده
                    continue  # بدون تاخیر، تلاش مجدد
                else:
                    # پس از 5 تلاش ناموفق، تصویر را نادیده بگیر
                    return None
            else:
                # برای خطاهای دیگر، پیام خطا ارسال شود
                raise Exception(f"خطا در پردازش تصویر {index}: {error_message}")
    return None