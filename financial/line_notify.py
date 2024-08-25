import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# 載入 .env 文件
load_dotenv("line_notify.env")

# 讀取 LINE Notify token
line_token = os.getenv("LINE_NOTIFY_TOKEN")

# 設定lineNotify
def lineNotify(line_token, msg):
    headers = {
        "Authorization": "Bearer " + line_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payload = {'message': msg}
    notify = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    return notify.status_code

def get_exchange_rate(api_url, base_currency='USD', target_currency='TWD'):
    """從匯率 API 獲取即時匯率價格"""
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        if base_currency in data['rates'] and target_currency in data['rates']:
            rate = data['rates'][target_currency] / data['rates'][base_currency]
            return rate
        else:
            print("Currency not found in the response.")
            return None
    else:
        print(f"Failed to get exchange rate: {response.status_code}")
        return None

# 組裝傳送到lineNotify的訊息
def sendline(mode, date, realprice, token):
    msg = f"\nMode: {mode}\nDate: {date}\nReal Price: {realprice}"
    
    # 發送通知
    status_code = lineNotify(token, msg)
    return status_code

# 獲取當前日期和時間
def get_current_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# 匯率 API URL
exchange_rate_api_url = "https://api.exchangerate-api.com/v4/latest/USD"  

# 獲取即時匯率價格
realprice = get_exchange_rate(exchange_rate_api_url, base_currency='USD', target_currency='TWD')

# 測試發送通知
if realprice:
    mode = "匯率轉換"
    date = get_current_date()  # 獲取當前日期和時間
    status_code = sendline(mode, date, f"{realprice:.2f}", line_token)
    print(f"Notification status code: {status_code}")
else:
    print("404")
