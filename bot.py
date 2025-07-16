import requests
import time
import datetime
import pytz
import telegram
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHAT_ID")
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
        headers = {
            'x-access-token': GOLD_API_KEY,
            'Content-Type': 'application/json'
        }
        r = requests.get('https://www.goldapi.io/api/XAU/USD', headers=headers)
        return float(r.json()['price'])
    except:
        return None

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
    bot = telegram.Bot(token=BOT_TOKEN)
    while True:
        if is_weekend_night():
            print("🛑 Cuối tuần, bot nghỉ...")
        else:
            btc = get_btc_price()
            xau = get_xauusd_price()
            now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%H:%M ngày %d tháng %m, %Y')
            if btc and xau:
                message = f"""🕒 {now}
Giá XAUUSD: ${xau:,.2f}
Giá BTC: ${btc:,.2f}"""
                bot.send_message(chat_id=CHANNEL_ID, text=message)
                print("✅ Đã gửi:", message)
            else:
                print("⚠️ Lỗi khi lấy giá")
        time.sleep(SLEEP_SECONDS)

if __name__ == '__main__':
    run_bot()
