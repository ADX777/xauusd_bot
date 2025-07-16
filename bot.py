import requests
import datetime
import pytz
import asyncio
from telegram import Bot
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHAT_ID')
GOLD_API_KEY = os.getenv('GOLD_API_KEY')

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
        if r.status_code == 200:
            data = r.json()
            return float(data['price'])
        else:
            print("⚠️ GoldAPI status:", r.status_code)
            return None
    except:
        return None

def is_weekend_night():
    now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    weekday = now.weekday()
    hour = now.hour
    return (weekday == 4 and hour >= 23) or weekday in [5, 6] or (weekday == 0 and hour < 7)

async def sleep_until_next_hour():
    now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    delta = (next_hour - now).total_seconds()
    print(f"⏳ Đợi {int(delta)} giây đến {next_hour.strftime('%H:%M')}...")
    await asyncio.sleep(delta)

async def run_bot():
    bot = Bot(token=BOT_TOKEN)
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
                await bot.send_message(chat_id=CHANNEL_ID, text=message)
                print("✅ Đã gửi:", message)
            else:
                print("⚠️ Lỗi khi lấy giá")
        await sleep_until_next_hour()

if __name__ == '__main__':
    asyncio.run(run_bot())
