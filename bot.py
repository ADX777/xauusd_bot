import requests
import datetime
import pytz
import asyncio
from telegram import Bot
import os

# Lấy token, chat ID và API key từ biến môi trường
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHAT_ID')
GOLD_API_KEY = os.getenv('GOLD_API_KEY')

# Hàm lấy giá BTC từ Binance
def get_btc_price():
    try:
        r = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
        return float(r.json()['price'])
    except Exception as e:
        print("❌ Lỗi lấy giá BTC:", e)
        return None

# Hàm lấy giá vàng XAU/USD từ GoldAPI
def get_xauusd_price():
    try:
        headers = {'x-access-token': GOLD_API_KEY}
        r = requests.get('https://www.goldapi.io/api/XAU/USD', headers=headers)
        if r.status_code == 200:
            return float(r.json()['price'])
        print("⚠️ GoldAPI trả về mã lỗi:", r.status_code)
        return None
    except Exception as e:
        print("❌ Lỗi lấy giá vàng:", e)
        return None

# Hàm chính chạy mỗi giờ
async def run_bot_once():
    now_dt = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    weekday = now_dt.weekday()
    hour = now_dt.hour

    # Điều kiện không gửi (nghỉ cuối tuần và ban đêm)
    if (weekday == 4 and hour >= 23) or weekday in [5, 6] or (weekday == 0 and hour < 7):
        print("🛑 Không gửi: cuối tuần hoặc ngoài khung giờ.")
        return

    bot = Bot(token=BOT_TOKEN)
    btc = get_btc_price()
    xau = get_xauusd_price()
    now_str = now_dt.strftime('%H:%M ngày %d tháng %m, %Y')

    if btc and xau:
        message = f"""🕒 {now_str}
Giá XAUUSD: ${xau:,.2f}
Giá BTC: ${btc:,.2f}"""
        await bot.send_message(chat_id=CHANNEL_ID, text=message)
        print("✅ Đã gửi thành công lúc", now_str)
    else:
        error_message = f"""⚠️ {now_str}
Không lấy được giá:
- XAU: {"OK" if xau else "LỖI"}
- BTC: {"OK" if btc else "LỖI"}"""
        await bot.send_message(chat_id=CHANNEL_ID, text=error_message)
        print("❌ Lỗi gửi giá, đã báo vào Telegram.")

# Khởi chạy
if __name__ == '__main__':
    asyncio.run(run_bot_once())
