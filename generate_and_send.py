import os, requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
PROMPT = os.environ.get("PROMPT", "A cinematic mountain landscape at golden hour, photorealistic, 4k")

def generate():
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(PROMPT)}?width=1024&height=1024&nologo=true"
    res = requests.get(url, timeout=60)
    res.raise_for_status()
    return res.content

def send(img):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    res = requests.post(url, data={"chat_id": CHAT_ID, "caption": PROMPT}, files={"photo": ("img.jpg", img, "image/jpeg")})
    res.raise_for_status()

if __name__ == "__main__":
    print("🎨 Generating...")
    img = generate()
    print("📤 Sending to Telegram...")
    send(img)
    print("✅ Done.")
