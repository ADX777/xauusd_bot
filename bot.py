

import requests
import time
import datetime
import pytz
import telegram
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GOLD_API_KEY = os.getenv("GOLD_API_KEY")

def get_btc_price():
    try:
        r = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
        return float(r.json()['price'])
    except:
        return None

def get_xauusd_price():
    try:
        r = requests.get(
            'https://www.goldapi.io/api/XAU/USD',
            headers={'x-access-token': GOLD_API_KEY, 'Content-Type': 'application/json'}
        )
        data = r.json()
        return float(data['price'])
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

def seconds_until_next_hour():
    now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    return (next_hour - now).total_seconds()

def run_bot():
    bot = telegram.Bot(token=BOT_TOKEN)
    while True:
        if is_weekend_night():
            print("🛑 Cuối tuần, bot nghỉ...")
        else:
            btc = get_btc_price()
            xau = get_xauusd_price()
            now_str = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%H:%M | Ngày %d/%m/%Y')

            if btc and xau:
                message = f"""📢 [FOREX LIVE] Cập nhật giá mới nhất:

🟡 Vàng (XAUUSD): ${xau:,.2f}
🟠 Bitcoin (BTC): ${btc:,.2f}

🕒 Thời gian: {now_str}
"""
                bot.send_message(chat_id=CHANNEL_ID, text=message)
                print("✅ Đã gửi:\n", message)
            else:
                print("⚠️ Lỗi khi lấy giá")

        sleep_time = seconds_until_next_hour()
        print(f"⏳ Chờ {sleep_time:.0f} giây tới giờ tròn tiếp theo...\n")
        time.sleep(sleep_time)

if __name__ == '__main__':
    run_bot()
