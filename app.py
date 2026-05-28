import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

BOT_TOKEN      = os.environ.get("BOT_TOKEN", "")
OWNER_ID       = int(os.environ.get("OWNER_ID", "5851560671"))
HF_TOKEN       = os.environ.get("HF_TOKEN", "")
HF_MODEL       = "mistralai/Mistral-7B-Instruct-v0.3"

SYSTEM_PROMPT = """You are the smart assistant of Ilia Rezaei. Always reply in Persian (Farsi).

About Ilia:
- Name: ایلیا رضایی (Ilia Rezaei)
- Age: 18 years old
- City: Yazd, Iran
- Experience: 1.5+ years in networking and IT

Services:
• Network setup with MikroTik and Cisco
• CCTV installation and configuration
• Linux server management (Ubuntu, Debian, CentOS)
• Windows Server (Active Directory, DNS, DHCP)
• Structured cabling Cat5e/Cat6
• Network troubleshooting and support

Rules:
- Always reply in Persian (Farsi) only
- Be polite and professional
- For pricing questions say they must contact Ilia directly
- Keep replies short and helpful (max 120 words)
- Always end with a suggestion to contact Ilia directly
"""

def send_telegram(chat_id, text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
            timeout=10,
        )
    except Exception:
        pass

def ask_ai(message):
    prompt = f"<s>[INST] {SYSTEM_PROMPT}\n\nUser: {message} [/INST]"
    try:
        r = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 300, "temperature": 0.7, "return_full_text": False}},
            timeout=30,
        )
        data = r.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        if isinstance(data, dict) and "error" in data:
            if "loading" in data["error"].lower():
                return "⏳ مدل در حال بارگذاری است. ۳۰ ثانیه دیگر دوباره امتحان کن."
        return "⚠️ مشکلی پیش اومد. مستقیم با ایلیا تماس بگیر."
    except Exception:
        return "⚠️ خطا در اتصال. لطفاً مستقیم با ایلیا تماس بگیر."

@app.route("/")
def index():
    return send_from_directory(".", "miniapp.html")

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.json or {}
    name    = data.get("name", "").strip()
    phone   = data.get("phone", "").strip()
    service = data.get("service", "").strip()
    message = data.get("message", "").strip()
    lang    = data.get("lang", "fa")

    if not name or not message:
        return jsonify({"ok": False, "error": "Missing fields"}), 400

    text = (
        f"📩 *درخواست جدید از Mini App*\n\n"
        f"👤 نام: {name}\n"
        f"📞 تلفن: {phone or 'ندارد'}\n"
        f"🛠 خدمات: {service or 'مشخص نشده'}\n"
        f"🌐 زبان: {'فارسی' if lang == 'fa' else 'English'}\n\n"
        f"💬 پیام:\n{message}"
    )
    send_telegram(OWNER_ID, text)
    return jsonify({"ok": True})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"ok": False, "error": "Empty message"}), 400
    reply = ask_ai(message)
    return jsonify({"ok": True, "reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
