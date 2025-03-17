import os, io, hashlib, base64, asyncio
import aiohttp
from PIL import Image
from rembg import remove
from config import STABILITY_URL, STABILITY_AUTH_TOKEN, CLOUDFLARE_URL, HEADERS, IMAGE_DIR

# اطمینان از وجود پوشه تصاویر
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

async def generate_image_cloudflare(prompt: str) -> str:
    payload = {"steps": 8, "prompt": prompt}
    async with aiohttp.ClientSession() as session:
        async with session.post(CLOUDFLARE_URL, headers=HEADERS, json=payload) as response:
            if response.status != 200:
                raise Exception(f"خطا در فراخوانی: {await response.text()}")
            result = await response.json()
            base64_image = result.get("result", {}).get("image")
            if not base64_image:
                raise Exception("خطا در دریافت تصویر")
            image_bytes = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_bytes))
            random_hash = hashlib.sha256(os.urandom(32)).hexdigest()
            filename = f"{random_hash}.jpg"
            filepath = os.path.join(IMAGE_DIR, filename)
            image.save(filepath)
            if not os.path.exists(filepath):
                raise Exception(f"فایل در مسیر {filepath} ذخیره نشد!")
            return filepath

async def generate_image_without_removal(prompt_json: dict) -> tuple:
    if not isinstance(prompt_json, dict):
        raise ValueError("ورودی باید دیکشنری باشد")

    if prompt_json.get("accurate", False):
        prompt = prompt_json.get("prompt", "")
        image_path = await generate_image_cloudflare(prompt)
    else:
        payload = {
            "guidance": prompt_json.get("guidance", 12),
            "height": prompt_json.get("height", 1024),
            "negative_prompt": prompt_json.get("negative_prompt", ""),
            "num_steps": prompt_json.get("steps", 20),
            "prompt": prompt_json.get("prompt", ""),
            "seed": prompt_json.get("seed", 52),
            "width": prompt_json.get("width", 1024)
        }
        headers = {
            'Authorization': STABILITY_AUTH_TOKEN,
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(STABILITY_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    image_data = await response.read()
                    random_hash = hashlib.sha256(os.urandom(32)).hexdigest()
                    filename = f"{random_hash}.jpg"
                    image_path = os.path.join(IMAGE_DIR, filename)
                    with open(image_path, "wb") as f:
                        f.write(image_data)
                    if not os.path.exists(image_path):
                        raise Exception(f"فایل اصلی در {image_path} ساخته نشد!")
                else:
                    raise Exception(f"خطا در دریافت تصویر: {response.status}")
    return image_path, False  # همیشه بک‌گراند حذف نشود

# تابع perform_background_removal را حذف می‌کنیم چون نیازی به حذف بک‌گراند نداریم