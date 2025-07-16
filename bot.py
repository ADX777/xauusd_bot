import requests
import time
import datetime
import pytz
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHAT_ID")  # Ví dụ: @forexlive777
GOLD_API_KEY = os.getenv("GOLD_API_KEY")
SLEEP_SECONDS = 3600

def get_btc_price():
    try:
        r = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
        return float(r.json()['price'])
    except:
        return None

def get_xauusd_price():
    try:
        headers = {'x-access-token': GOLD_API_KEY}
        r = requests.get('https://www.goldapi.io/api/XAU/USD', headers=headers)
        return float(r.json()['price'])
    except:
        return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": message
    }
    requests.post(url, data=data)

def is_weekend_night():
    now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    weekday = now.weekday()
    hour = now.hour
    if weekday == 4 and hour >= 23:
        return True
    if weekday == 5:
        return True
    if weekday == 6:
        return True
    if weekday == 0 and hour < 7:
        return True
    return False

def run_bot():
    while True:
        if is_weekend_night():
            print("🛑 Cuối tuần, bot nghỉ...")
        else:
            btc = get_btc_price()
            xau = get_xauusd_price()
            now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%H:%M ngày %d tháng %m, %Y')
            if btc and xau:
                message = f"""✅ Đã gửi: 🕒 {now}
Giá XAUUSD: ${xau:,.2f}
Giá BTC: ${btc:,.2f}"""
                send_telegram_message(message)
                print(message)
            else:
                print("⚠️ Lỗi khi lấy giá")
        time.sleep(SLEEP_SECONDS)

if __name__ == '__main__':
    run_bot()
