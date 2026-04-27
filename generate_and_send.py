import os, requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
PROMPT = os.environ.get("PROMPT", "A cinematic mountain landscape, photorealistic, 4k")

def generate():
    print(f"🎨 Generating: {PROMPT}")
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(PROMPT)}?width=1024&height=1024&nologo=true"
    res = requests.get(url, timeout=60)
    res.raise_for_status()
    print("✅ Image generated")
    return res.content

def send(img):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    print(f"📤 Sending to chat_id: {CHAT_ID}")
    
    # تست اتصال به تلگرام
    test_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    test_res = requests.get(test_url)
    if test_res.status_code != 200:
        raise Exception(f"❌ BOT_TOKEN اشتباه است! پاسخ: {test_res.text}")
    
    bot_info = test_res.json()
    print(f"✅ ربات فعال است: @{bot_info['result']['username']}")
    
    # ارسال عکس
    res = requests.post(url, data={"chat_id": CHAT_ID, "caption": PROMPT}, 
                       files={"photo": ("img.jpg", img, "image/jpeg")})
    
    if res.status_code == 400:
        error_msg = res.json().get('description', 'Unknown error')
        raise Exception(f"❌ خطا در ارسال: {error_msg}\nCHAT_ID: {CHAT_ID}\nآیا به ربات استارت زده‌اید؟")
    elif res.status_code == 401:
        raise Exception(f"❌ BOT_TOKEN اشتباه است!")
    
    res.raise_for_status()
    print("✅ Sent successfully!")

if __name__ == "__main__":
    try:
        img = generate()
        send(img)
        print("🎉 Done!")
    except Exception as e:
        print(str(e))
        raise
