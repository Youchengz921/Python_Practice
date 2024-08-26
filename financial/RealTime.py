import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import time

# 讀取lineNotify token
load_dotenv("line_notify.env")
line_token = os.getenv("test_robot_token")

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

# 組裝傳送到lineNotify的訊息
def sendline(date, threshold, realprice, token):
    msg = (
            f"\n"
            f"Mode: 匯率監測\n"
            f"現在時間: {date}\n"
            f"警告 ! 當前匯率已低於 {threshold}!\n"
            f"當前匯率: {realprice:.2f}"
          )
    
    # 發送通知
    status_code = lineNotify(token, msg)
    return status_code

# 當前日期和時間
def get_current_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# 匯率 API URL
exchange_rate_api_url = "https://api.exchangerate-api.com/v4/latest/USD"

# 監測數值
threshold_value = float(input("請輸入匯率監測的值 (例如 30.00): "))

# 間隔秒數
wait_time = 600

# 設定通知次數
max_notifications = 3    # 最大通知數
notification_count = 0   

while notification_count < max_notifications:
    # 獲取即時匯率價格
    realprice = get_exchange_rate(exchange_rate_api_url, base_currency='USD', target_currency='TWD')
    if realprice:
        date = get_current_date()
        if realprice < threshold_value:
            msg = sendline(date, threshold_value, realprice, line_token)
            notification_count += 1
            print(f"Notification {notification_count} status code: {msg}")
        else:
            print(f"目前匯率: {realprice:.2f}")
    else:
        print("Failed to retrieve exchange rate.")
    
    # 等待指定的時間間隔後再測量
    time.sleep(wait_time)

print("已達到最大通知次數，程式結束。")
