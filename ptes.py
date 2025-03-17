import base64
import os
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""درخت"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""```json
{
    \"prompts\": [
        {
            \"prompt\": \"A majestic oak tree standing alone in a golden wheat field, bathed in the warm light of the setting sun. The tree's branches are reaching towards the sky, with leaves rustling gently in the breeze. Focus on the intricate details of the bark and leaves, capturing the texture and depth of the tree. Use a shallow depth of field to blur the background and draw attention to the tree. Photorealistic, 8k, 35mm f/1.8 lens, cinematic lighting, warm color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"A twisted and ancient olive tree clinging to a rocky cliff overlooking the turquoise Mediterranean Sea. The tree's gnarled branches are a testament to its age and resilience. Capture the contrast between the rough texture of the bark and the smooth, shimmering surface of the water. Use a wide-angle lens to capture the vastness of the landscape. Photorealistic, 8k, 14mm f/2.8 lens, natural lighting, cool color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"A vibrant cherry blossom tree in full bloom, with delicate pink petals covering its branches. The tree is set against a backdrop of traditional Japanese architecture, creating a serene and peaceful scene. Focus on the soft, diffused light filtering through the petals. Photorealistic, 8k, 50mm f/1.4 lens, soft lighting, pastel color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"A towering redwood tree reaching towards the sky in a misty forest. The tree's massive trunk is covered in thick, reddish-brown bark, and its branches are home to a variety of birds and other wildlife. Capture the scale and grandeur of the tree, emphasizing its height and age. Photorealistic, 8k, 24mm f/2.8 lens, atmospheric lighting, earthy color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"A lone palm tree silhouetted against a vibrant sunset sky on a tropical beach. The tree's fronds are swaying gently in the breeze, and its trunk is casting a long shadow across the sand. Capture the warmth and beauty of the tropical landscape. Photorealistic, 8k, 85mm f/1.8 lens, golden hour lighting, warm color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"A bare winter tree covered in frost and snow, standing in a desolate landscape. The tree's branches are stark and skeletal, and its trunk is dusted with snow. Capture the cold and bleak beauty of the winter scene. Photorealistic, 8k, 35mm f/2.0 lens, winter lighting, cool color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        }
    ],
    \"caption\": \"درود👋! این تصاویر با الهام از درخواست شما مبنی بر تولید عکس از درختان خلق شده‌اند. در این مجموعه، تلاش شده تا درختان در موقعیت‌ها و فصل‌های مختلف به تصویر کشیده شوند. از درخت بلوط در دشت طلایی گرفته تا درخت زیتون در صخره‌های مدیترانه، هر تصویر داستان و زیبایی خاص خود را دارد. این تصاویر با استفاده از تکنیک‌های پیشرفته عکاسی و نورپردازی حرفه‌ای ایجاد شده‌اند تا حس و حال واقعی طبیعت را به شما منتقل کنند.\\n\\nپیشنهاد می‌کنم در پرامت بعدی، به درختان خاصی مانند 'درخت بائوباب در غروب آفتاب آفریقا' یا 'درخت سرو در یک قبرستان قدیمی' اشاره کنید. همچنین می‌توانید از سبک‌های هنری خاصی مانند 'امپرسیونیسم' یا 'سوررئالیسم' برای خلق تصاویر متفاوت بهره ببرید. به این شکل تصاویر زیباتر و جذاب‌تری خواهید داشت.😉🌳🎨\\n\\nهمچنین، برای الهام‌بخشیدن به تصاویر خود، می‌توانید از این پرامت پیشنهادی استفاده کنید: 'A majestic ancient oak tree, its branches reaching towards a stormy sky, lightning illuminating its gnarled trunk. Ray tracing, volumetric lighting, dramatic composition.' ✨📸🌩️\\n\\nبا تشکر از سلیقه زیباتون😊🙏\",
    \"base_prompt\": \"A majestic oak tree standing alone in a golden wheat field, bathed in the warm light of the setting sun. The tree's branches are reaching towards the sky, with leaves rustling gently in the breeze. Focus on the intricate details of the bark and leaves, capturing the texture and depth of the tree. Use a shallow depth of field to blur the background and draw attention to the tree. Photorealistic, 8k, 35mm f/1.8 lens, cinematic lighting, warm color palette.\",
    \"suggestion\": \"تلاش کنید در پرامت‌های بعدی، بافت‌های مختلف را توصیف کنید تا تصاویر با جزئیات بیشتری ایجاد شوند.😊\"
}
```"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""سگ"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""```json
{
    \"prompts\": [
        {
            \"prompt\": \"A golden retriever puppy playing in a field of wildflowers, bathed in the soft light of the late afternoon sun. Focus on the puppy's playful expression and the vibrant colors of the flowers. Use a shallow depth of field to blur the background and draw attention to the puppy. Photorealistic, 8k, 35mm f/1.8 lens, cinematic lighting, warm color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"A majestic Siberian husky standing on a snowy mountain peak, with a piercing gaze and a windswept coat. Capture the dog's strength and resilience in the face of the harsh winter landscape. Use a wide-angle lens to capture the vastness of the surroundings. Photorealistic, 8k, 14mm f/2.8 lens, natural lighting, cool color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"A playful French bulldog puppy wearing a colorful bandana, sitting in a cozy armchair in a sunlit living room. Focus on the puppy's adorable expression and the details of its wrinkled face. Use a 50mm lens to capture the intimate setting. Photorealistic, 8k, 50mm f/1.4 lens, soft lighting, warm color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"A loyal German shepherd working dog standing guard in a misty forest, its alert eyes scanning the surroundings. Capture the dog's intelligence and dedication, emphasizing its muscular build and focused expression. Use atmospheric lighting to create a sense of mystery. Photorealistic, 8k, 24mm f/2.8 lens, atmospheric lighting, earthy color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"A friendly Labrador retriever swimming in a clear blue lake, its tongue lolling out in enjoyment. Capture the dog's energy and enthusiasm for life, emphasizing its wet fur and splashing water. Use a high shutter speed to freeze the action. Photorealistic, 8k, 85mm f/1.8 lens, bright sunlight, vibrant color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        },
        {
            \"prompt\": \"An elderly beagle sleeping peacefully on a soft blanket, its face etched with wrinkles and its paws twitching in a dream. Capture the dog's peacefulness and contentment, emphasizing its gentle nature and the warmth of the surrounding environment. Photorealistic, 8k, 35mm f/2.0 lens, soft indoor lighting, warm color palette.\",
            \"accurate\": true,
            \"remove\": false,
            \"steps\": 8
        }
    ],
    \"caption\": \"سلام رفیق😊! این تصاویر زیبا از سگ‌ها، با الهام از درخواست شما تولید شده‌اند. در این مجموعه، تلاش شده تا سگ‌ها در نژادها و موقعیت‌های مختلف به تصویر کشیده شوند. از توله‌های بازیگوش گرفته تا سگ‌های نگهبان وفادار، هر تصویر داستانی خاص خود را دارد.🐾🏡🐕\\n\\nپیشنهاد می‌کنم در پرامت بعدی، به حالت‌های خاصی از سگ‌ها مانند 'سگی که در حال انجام یک ترفند است' یا 'سگی که در یک مسابقه شرکت کرده' اشاره کنید. همچنین می‌توانید از زوایای دید خاصی مانند 'نمای از پایین' یا 'نمای از نزدیک' برای خلق تصاویر متفاوت بهره ببرید. به این شکل تصاویرتون جذاب‌تر میشه.✨\\n\\nهمچنین، برای الهام‌بخشیدن به تصاویر خود، می‌توانید از این پرامت پیشنهادی استفاده کنید: 'A majestic German Shepherd, standing proudly in a field of golden wheat, bathed in the warm light of the setting sun. Film grain, soft shadows, dramatic lighting.' 🌾☀️🐕\\n\\nممنون از انتخاب زیباتون.🙏\",
    \"base_prompt\": \"A golden retriever puppy playing in a field of wildflowers, bathed in the soft light of the late afternoon sun. Focus on the puppy's playful expression and the vibrant colors of the flowers. Use a shallow depth of field to blur the background and draw attention to the puppy. Photorealistic, 8k, 35mm f/1.8 lens, cinematic lighting, warm color palette.\",
    \"suggestion\": \"بهتره توی پرامت‌های بعدی، از لنزهای مختلف استفاده کنی تا نتایج متنوع‌تری ببینی.😉\"
}
```"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_modalities=[
            "text",
        ],
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_LOW_AND_ABOVE",  # Block most
            ),
        ],
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""دستور :
                                       متن زیر رو به صورت یک پرامت مفهومی انگلیسی به جهت تولید یک عکس بازنویسی و هیچ تغییری توی مفهومش نده:
                                       متن پرامت شماره 1:
                                       [{user_text}]
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
                            توجه: برای زیبایی هرچه بیشتر پرامت از لیست پیشنهادی زیر کمک بگیر:
                           {Suggestions}
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
                                       نکته آخر : جیسون رو به صورت متن خالی بده و نیاز به فرستادن در قالب جیسون نیست
                                       یعنی به هیچ عنوان نباید [```json] اینجور بفرستی
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

متغییر ها :

mass = '''
تصاویر شما با موفقیت درون کانال قرار گرفتن :

https://t.me/MahoAi_image
'''

PRECISE_JSON = \"\"\"
{
    \"prompt\": \"\",
    \"accurate\": true,
    \"remove\": false,
    \"steps\": 8,
}
\"\"\"

CREATIVE_JSON = \"\"\"
{
    \"prompt\": \"\",
    \"accurate\": false,
    \"remove\": false,
    \"negative_prompt\": \"\",
    \"width\": 1024,
    \"height\": 1024,
    \"steps\": 20,
    \"guidance\": 12,
    \"seed\": 52
}
\"\"\"

  base_json2 = \"\"\"
 {
    \"prompts\": [],
    \"caption\": \"\"
}"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        if chunk.candidates[0].content.parts[0].inline_data:
            file_name = "ENTER_FILE_NAME"
            save_binary_file(
                file_name, chunk.candidates[0].content.parts[0].inline_data.data
            )
            print(
                "File of mime type"
                f" {chunk.candidates[0].content.parts[0].inline_data.mime_type} saved"
                f"to: {file_name}"
            )
        else:
            print(chunk.text)

if __name__ == "__main__":
    generate()
