import json
import aiohttp
from .fix_json import fix_and_parse_json
from .check import check
import os
from dotenv import load_dotenv


load_dotenv()
GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT")
mass = '''
تصاویر شما با موفقیت درون کانال قرار گرفتن :

https://t.me/MahoAi_image
'''

PRECISE_JSON = """
{
    "prompt": "",
    "accurate": true,
    "remove": false,
    "steps": 8,
}
"""

CREATIVE_JSON = """
{
    "prompt": "",
    "accurate": false,
    "remove": false,
    "negative_prompt": "",
    "width": 1024,
    "height": 1024,
    "steps": 20,
    "guidance": 12,
    "seed": 52
}
"""

async def generate_prompts(user_text, mode="precise"):
    if mode == "precise":
        base_json = PRECISE_JSON
    else:
        base_json = CREATIVE_JSON

    prompts_js = await check(user_text)
    Advertising = prompts_js["Advertising"]
    caption = prompts_js["caption"]
    nudity = prompts_js["nudity"]
    Suggestions = json.dumps(prompts_js["Suggestions"], ensure_ascii=False, indent=4)

    if nudity:
        return [], caption, Advertising

    base_json2 = """
 {
    "prompts": [],
    "caption": ""
}
"""
    list1= f"""توجه: برای زیبایی هرچه بیشتر پرامت از لیست پیشنهادی زیر کمک بگیر:
                           {Suggestions}
    """
    nokte = """
           نکانتی که برای تولید یک پرامت خوب باید در نظر بگیری:[
                         🔹 افزایش عمق فنی با اصطلاحات سینمایی/عکاسی:
                        ✅ نورپردازی پیشرفته:
                        Subsurface Scattering (SSS) → برای طبیعی‌تر کردن پوست و مواد نیمه‌شفاف
                        Volumetric Lighting → نور حجمی برای نمایش پرتوهای نور و مه
                        Global Illumination (GI) → نورپردازی سراسری برای واقعی‌تر شدن سایه‌ها
                        Ambient Occlusion (AO) → سایه‌های محیطی برای افزایش عمق
                        Ray Tracing → محاسبه دقیق بازتاب‌ها و انکسارهای نوری
                        Caustics → بازتاب‌های نوری روی آب و شیشه
                        ✅ افکت‌های لنز و شبیه‌سازی دوربین:
                        Chromatic Aberration → انحراف رنگی برای حس سینمایی
                        Depth of Field (DOF) → محو کردن پس‌زمینه برای جداسازی سوژه
                        Bokeh Shapes → تنظیم شکل بوکه (دایره‌ای، چندضلعی، آنامورفیک)
                        Anamorphic Lens Flare → بازتاب‌های مخصوص لنزهای سینمایی
                        Film Grain & Noise → شبیه‌سازی نویز فیلمی برای حس طبیعی‌تر
                        Motion Blur → تاری حرکت برای حس سرعت و پویایی
                        Long Exposure → نوردهی طولانی برای جلوه‌های خاص مثل رد نور خودرو
                        ✅ مدل‌سازی و فیزیک نور:
                        PBR Materials (Physically Based Rendering) → متریال‌های مبتنی بر فیزیک
                        Subpixel Rendering → افزایش دقت نمایش جزئیات
                        Light Falloff & Soft Shadows → محاسبه افت نور و سایه‌های نرم
                        Exposure Control → کنترل میزان نوردهی برای تأثیر احساسی بیشتر
                        🔹 اتصال عناصر به حس و مفهوم:
                        ✅ رنگ و احساس:
                        رنگ‌های سرد (آبی، خاکستری، بنفش کم‌رنگ) → احساس تنهایی، ترس، یا رمزآلودگی
                        رنگ‌های گرم (قرمز، نارنجی، طلایی) → حس انرژی، خشم، یا صمیمیت
                        رنگ سبز → آرامش، طبیعت، یا حس فراواقعی
                        تضاد شدید بین نور و تاریکی → دوگانگی خیر و شر
                        استفاده از مه و نور کم → حس رمزآلود و مبهم
                        ✅ زاویه دوربین و حس آن:
                        زاویه پایین (Low Angle) → نمایش قدرت و تسلط
                        زاویه بالا (High Angle) → نمایش ضعف و کوچکی شخصیت
                        نمای بسته (Close-up) → تأکید بر احساسات و واکنش‌ها
                        نمای فوق‌عریض (Extreme Wide Shot) → نشان دادن ناچیز بودن شخصیت در محیط
                        ✅ نورپردازی احساسی:
                        نور نرم و پخش‌شده → صمیمیت، آرامش، یا حس رویایی
                        نور سخت با سایه‌های تیز → تنش، ترس، یا استرس
                        نور پس‌زمینه (Backlight) → حس رمزآلود یا دراماتیک
                        نورپردازی کم‌کنتراست (Low Contrast Lighting) → حس مالیخولیا یا سردرگمی
                        🔹 استراتژی‌های کنترل خروجی AI:
                        Gradient-based Attention Weighting → کنترل تمرکز مدل در نواحی خاص
                        Multi-pass Refinement → پردازش چند مرحله‌ای برای افزایش کیفیت
                        Seed Control & Variability Reduction → کنترل خروجی تصادفی برای نتایج مشابه
                        Latent Space Navigation → هدایت مدل در فضای ویژگی‌ها برای خروجی خاص‌تر
                        Negative Prompting → جلوگیری از تولید عناصر ناخواسته
                        🔹 نمادگرایی روایی برای انتقال مفاهیم انتزاعی:
                        آینه → خودشناسی، تضاد درونی
                        سایه‌های کشیده → تهدید، ناامنی
                        دایره و حلقه → بی‌پایانی، چرخه‌های زمانی
                        زنجیر و طناب → محدودیت، اسارت، یا ارتباط عاطفی
                        انعکاس در آب → واقعیت موازی یا دوگانگی شخصیت
                        🔹 بهینه‌سازی واژگان برای کاهش ابهام:
                        ✅ اصطلاحات سینمایی:
                        35mm f/1.4 Lens → برای پرتره‌های حرفه‌ای
                        14mm f/2.8 Lens → برای ثبت چشم‌اندازهای سینمایی
                        3200K Warm Light → برای نور طلایی و صمیمانه
                        5600K Daylight → نور طبیعی و متعادل
                        ✅ سبک‌های سینمایی:
                        Film Noir → تاریکی و سایه‌های عمیق برای فضای معمایی
                        Cyberpunk → نورهای نئونی با ترکیب تکنولوژی و دیستوپیایی
                        Gothic Horror → استفاده از معماری تاریک و مه برای ترس و وحشت
                        🔹 یکپارچه‌سازی محدودیت‌های صریح برای جلوگیری از خروجی ناخواسته:
                        محدود کردن رنگ‌های غیرواقعی برای جلوگیری از افکت‌های عجیب
                        کنترل بیشترین و کمترین میزان جزئیات در تصویر
                        جلوگیری از اعوجاج غیرواقعی در پرسپکتیو شخصیت‌ها
                        🔹 لایه‌بندی سه‌بعدی محیط:
                        پیش‌زمینه (Foreground): عناصر نزدیک به دوربین که حس عمق می‌دهند
                        میان‌زمینه (Midground): سوژه اصلی که تمرکز روی آن است
                        پس‌زمینه (Background): ایجاد فضای محیطی و حس مقیاس
                        🔹 افزودن اصول ترکیب‌بندی سینمایی:
                        ✅ تکنیک‌های قاب‌بندی:
                        Rule of Thirds → تقسیم قاب به ۹ قسمت برای تعادل بصری
                        Leading Lines → هدایت چشم بیننده با خطوط راهنما
                        Golden Ratio → استفاده از نسبت طلایی برای ترکیب‌بندی طبیعی
                        Dutch Angle → کج کردن قاب برای ایجاد حس اضطراب
                        ✅ استفاده از فضای منفی:
                        Negative Space → حذف المان‌های غیرضروری برای تأکید روی سوژه
                        ✅ تکنیک‌های کنتراست:
                        High Contrast → نمایش دوگانگی و تنش بالا
                        Soft Contrast → ایجاد حس رویایی و لطیف
                        🔹 ایجاد حس حرکت و پویایی در صحنه:
                        ✅ افکت‌های سینمایی برای نمایش حرکت:
                        Motion Blur → تاری حرکت برای حس سرعت
                        Parallax Scrolling → اختلاف‌منظر برای عمق بیشتر
                        Dynamic Lighting → نورپردازی متحرک برای تأثیر احساسی
                        ✅ افکت‌های خاص برای تأثیرگذاری بیشتر:
                        Long Exposure Photography → ثبت حرکت نورها در شب
                        Tilt-shift Effect → ایجاد افکت مینیاتوری
                        Dual-focus Composition → دو نقطه فوکوس همزمان
                        ✅ تکنیک‌های نورپردازی خاص:
                        Underexposure → کم‌نوردهی برای حس رازآلودی
                        Overexposure → نور بیش از حد برای ایجاد حس استرس یا سرگیجه
                        🔹 استفاده از بافت‌ها و فیزیک نور برای عمق بیشتر:
                        Microdetail Mapping → اضافه کردن بافت‌های بسیار ریز
                        Ray-traced Shadows → سایه‌های واقع‌گرایانه و دقیق
                        Soft Diffusion Glow → نورهای ملایم برای حس فانتزی
                            ]
    """
    PR = f"""
                                       متن  رو به صورت یک پرامت مفهومی انگلیسی به جهت تولید یک عکس بازنویسی و هیچ تغییری توی مفهومش نده:
                                       [دستور: هیچ وقت حداکثر طول پرامت نباید بیش از 2048 کاراکتر بشه] 
                                       نکته : پرامت رو میتونی به شرط عوض نشدن خواسته و مفهوم گسترش بدی و پیرامون پرامت شرایط رو کامل توضیح بدی
                                       باید خواسته کاربر از این پرامت درک کنی و پس از درک خواسته کاربر ، پرامت رو پیرامون خواسته کاربر گسترش بدی
                                       می‌تونی تا جای ممکن به نسبت پرامت شرایط محیط تصویر خواسته شده توصیف کنی و خودت رو در شرایط پرامت بزاری و کامل توصیف کنی با تمامی تکنیک های طراحی
                                       میتونی پرامت رو زیبا سازی کنی و از انواع شرایط برای زیباتر شدن بهره بگیری
                                       میتونی متناسب با موضوع پرامت فضا سازی حرفه ای انجام بدی
                                       میتونی متناسب با موضوع پرامت بافت توصیف کنی و به توصیف جزئیات بسیار دقت کنی
                                       میتونی حالت نگاه سوژه و کاراکتر ها و زاویه دوربین رو توی بهترین حالت توصیف کنی
                                       میتونی پرامت برای پرامت شرایط نور پردازی حرفه ای توصیف کنی
                                       میتونی برای پرامتن ژست ها و حالات برای القای حس واقعی پرامت توصیف کنی
                                       میتونی از زاویه های متفاوت به پرامت نگاه کنی
                                       میتونی فوکوس پرامت رو روی سوژه اصلی بزاری
                                       میتونی بهترین رنگ بندی برای اجزای پرامت انتخاب کنی
                                       میتونی از رنگ های مکمل حرفه ای استفاده کنی
                                       میتونی بهترین مکان هارو برای پرامت بازگو کنی
                                       میتونی سبک تولید عکس رو متناسب با اهترین خروجی انتخاب کنی از خودت
                                       ترجیحا سبک خروجی نقاشی و امثالش نباشه 
                                       مهم:
                                    [هیج پرامتی با سبک کودکانه و یا 2 بعدی کودکانه و کارتونی و یا چند رنگ ثابت ایجاد نکن]
                                    نکته:  اگه خواستی عکس زن بسازی، به هیچ عنوان نباید خط سینه مشخص باشه و لباس باید بالا تر از سینه زن باشه حتما
                                       ترجیحا سبک های واقعی و انیمیشنی و 3 بعدی و بین این ها رو انتخاب کن
                                       میتونی توی پرامت نویسیت از زبان بدن بهره بگیری و برای کاراکتر ها زبان بدن رو کامل توصیف کنی
                                       میتونی حال و هوای پرامت متناسب با بهترین خروجی کامل توصیف کنی
                                       میتونی برای بهترین خروجی از کار به پرامت جهت بدی و روشن سازی کنیی
                                       میتونی به حالت مو و نوع پوشش دقت کنی و همه تلاشت برای توصیف ریز ترین جزئیات بهره بگیری
                                       همیشه سعی کن 1 سوژه داشته باشی توی پرامت و تمرکز اصلی روی سوژه اصلی فقط باشه
                                       میتونی متناسب با شرایط به توصیف المان ها بپردازی تا خروجی چشم نواز تر بشه
                                       مهم : از کلمات پر معنا و دارای معنای دقیق انگلیسی برای توصیف استفاده کن
                                       از حالت تمثیل و مثال زدن برای انتقال بهتر مفهوم پرامت بهره بگیر
                            خیلی مهم : اول عنوان پرامت رو درک کن و خواسته پرامت بفهم و بعد از تکنیک های بالا متناسب با خواسته و در صورت نیاز استفاده کن
                                       مهم: لباس زنان توی پرامت باید کاملا پوشیده تعریف شه حتما و برای زنان پوشش هایی بلند از گلو تا پا تعریف کن
                                       نکته مهم : شرایط تعریف شده در پرامت بر هر چیزی الویت داره و نباید توصیفت با شرایط تعریف شده در تضاد باشه
                                       باید برای پر کردنش متناقض پرامت رو بگی و همچنین روی ویژگی های اشتباهی که یک تصویر می‌تواند داشته باشد توصیف کنی
                                       ساختار جیسونی که باید به من بدی :
                                       {base_json}
                                       توجه : فقط و فقط و فقط دقیقا مثل جیسون بالا رو در نهایت بهم بده و نیاز به هیچ توضیحی ندارم و دقت کن ساختار جیسون با فاصله خراب نکنی دقیقا جیسون خروجی رو با فرمت جیسون صحیح نیاز دارم
                                       از ابعاد کاملا استاندارد استفاده کن
                                       نکته : توی متن پرامت توی جیسون اصلا نرو خط بعدی و متن یکپارچه و بدون هیچ فاصله ای باشه
                                       مهم ترین نکته که کامل باید دقت کنی:
                                       به هیچ عنوان توی متن پرامتت نباید فاصله رفتن به خط بعدی باشه چون ساختار جیسون خراب میشه
                                       دستور نهایی : یک آرایه به تعداد تصاویر درخواستی کاربر که توی متن پرامت گفته شده از جیسون بساز و اگه نگفته بود توی پرامت 6 تا در نظر بگیر و دقت کن حتما تعداد رو از متن پرامت پیدا کنی و اگه بیشتر از 10 گفته شده بود تو 10 تا بساز
                                       اگه کاربر شرایط هر تصویر رو توصیف کرده بود ، پرامتی که می‌سازی باید با شرایط توصیفی برای هر عکس دقیق باشد و هر پرامت رو با پرامت سایر تصاویر ترکیب نکنی و برای هر عکس پرامت یونیک خودش ایجاد کنی
                                       تعداد تصاویر رو توی پرامت ها دخیل نکن و هر پرامت باید روی سوژه یونیک خودش تمرکز داشته باشد
                                       نکته خیلی مهم : هیچ وقت طول آرایه بیشتر از 10 نباید بشه و حداکثر 10 تا باشه
                                       نکته : مقدار پرامت توی هیچ آیتمی از آرایه نباید با مقدار پرامت سایر آرایه ها برابر باشه و باید برای هر آیتم از آرایه یک پرامت یونیک بسازی
                                       حال آرایه رو داخل جیسون زیر قرار بده:
                                       {base_json2}
                                       مقدار کپشن رو با یه توضیح کامل و توصیف تصاویری که ساختی به زبان فارسی پر کن 
                                       میتونی با کاربر پیشنهاد بدی توی پرامت بعدیش ازت چی بخواد در موضوعات مختلف و مشابه با پرامت شماره 1 کاربر
                                       میتونی از کاربر بخاطر صلیقش تعریف کنی
                                       میتونی یه پرامت مشابه پرامت کاربر ولی به صورت بهبود یافته به کاربر پیشنهاد بدی برای زیباتر شدن تصاویرش و پیشنهادت فارسی باشه
                                       میتونی انواع مختلف پرامت ، مشابه پرامت کاربر ، بهش پینهاد بدی ولی پیشنهاداتت باید کاملا فارسی باشن
                                       میتونی یا شناخت صلیقه کاربر یک پرامت متفاوت از پرامت فعلی کاربر پیشنهاد بدی و بخوای که اینو هم امتحان کنه
                                       میتونی یکی از پرامت های لیست پیشنهادی رو با خلاقیت بیشتر به کاربر بگی
                                       میتونی ایرادات پرامت کاربر رو بهش بگی و راهنماییش کنی چجوری پرامت بهتری بنویسد و تکنیک های پرامت نویسی یادش بدی
                                       باید کاربر به همه هر بخش از متن داری توصیف می‌کنی پیشنهاد میدی و یا تعریف می‌کنی پس باید متن گویا و واضح و بدون ابهام باشه
                                       میتونی از ایموجی‌های مناسب با موضوع پرامت برای زیباسازی استفاده کنی
                                       تا جای ممکن از ایموجی‌ها برای منتقل کردن حس خوب به کاربر بهره بگیری
                                       حتما باید ایموجی و 1 پرامت پیشنهادی حداقل به کاربر گفته بشه
                                       به کاربر متنی مشابه متن زیر با زیبا سازی و خلاقیت بیشتر بگو:
                                       {mass}
                                         """
    ch = """
    دستور : جیسونی که تولید میکنی 2 بار برسی کامل کن محتوای prompts و هر کجا توی پرامت ها صحبت از خانم بود واسش یک پوشش بلند از گلو تا نوک پا با مانتو دامن بلند توصیف کن
    """

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"Make the outputs in JSON format. {base_json2}"
                    } ,
                    {
                        "text": nokte
                    },
                    {
                        "text": list1
                    },
                    {
                        "text": PR
                    },
                    {
                        "text": ch
                    }
                ]
            },
            {"role": "user",
            "parts": [{"text": user_text}]
        }]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(GEMINI_ENDPOINT, json=payload) as response:
            response.raise_for_status()
            gemini_response = await response.json()
            generated_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
            prompts_bais = fix_and_parse_json(generated_text)
            prompts_array = prompts_bais['prompts']
            prompts_caption = prompts_bais['caption']
            prompts_Advertising = Advertising
            if not isinstance(prompts_array, list):
                raise ValueError("خروجی باید یک لیست باشد، نه یک رشته یا چیز دیگر.")
            if nudity == False:
                for prompt in prompts_array:
                    if not isinstance(prompt, dict):
                        raise ValueError("هر آیتم در لیست باید یک دیکشنری باشد.")
            return prompts_array, prompts_caption, prompts_Advertising
