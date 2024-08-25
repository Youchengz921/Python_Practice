import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import twstock

# 讀取lineNotify token
load_dotenv("line_notify.env")
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

# 獲取即時匯率價格
def get_exchange_rate(api_url, base_currency='USD', target_currency='TWD'):
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

# 獲取鴻海股票即時價格
def get_stock_price(stock_id='2317'):
    stock = twstock.Stock(stock_id)
    latest_price = stock.price[-1] if stock.price else None
    return latest_price

# 組裝傳送到lineNotify的訊息
def sendline(mode, date, value, token):
    msg = f"\nMode: {mode}\n現在時間: {date}\n金額: {value}"
    
    # 發送通知
    status_code = lineNotify(token, msg)
    return status_code

# 獲取當前日期和時間
def get_current_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# 匯率 API URL
exchange_rate_api_url = "https://api.exchangerate-api.com/v4/latest/USD"  

# 取得輸入的 mode
mode = input("請選擇 mode (1.匯率轉換 2.鴻海股票): ")

if mode == '1':
    # 獲取即時匯率價格
    realprice = get_exchange_rate(exchange_rate_api_url, base_currency='USD', target_currency='TWD')
    if realprice:
        date = get_current_date()  
        status_code = sendline("匯率轉換", date, f"{realprice:.2f}", line_token)
        print(f"Notification status code: {status_code}")
    else:
        print("Failed to retrieve exchange rate.")
elif mode == '2':
    # 獲取鴻海股票即時價格
    stock_price = get_stock_price(stock_id='2317')
    if stock_price:
        date = get_current_date()
        status_code = sendline("鴻海股票", date, f"{stock_price:.2f}", line_token)
        print(f"Notification status code: {status_code}")
    else:
        print("Failed to retrieve stock price.")
else:
    print("Invalid mode. Please enter '1' or '2'.")
