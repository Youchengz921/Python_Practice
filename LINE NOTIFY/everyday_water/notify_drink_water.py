import requests
import schedule
import time
import os
import json
from dotenv import load_dotenv
import logging

# 載入 .env 檔案
load_dotenv('line notify.env')

# 取得 LINE Notify API Token
Chose_API = input('1:個人訊息\n2:群組訊息\n:')

if Chose_API == '1':    
    LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')      # 個人TOKEN
    print('已使用個人喝水token')
elif Chose_API == '2':
    LINE_NOTIFY_TOKEN = os.getenv('GROUP_TOKEN')        # 群組TOKEN
    print('已使用群組喝水token')
LINE_NOTIFY_API_URL = 'https://notify-api.line.me/api/notify'

# 設定日誌檔案
log_dir = 'D:/vscode_python/python bible/LINE NOTIFY/everyday_water'
log_file = os.path.join(log_dir,'water_reminder.log')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 從 .json 檔案讀取提醒時間
json_file_path = os.path.join('everyday_water', 'water_config.json')
with open(json_file_path, 'r') as file:
    config = json.load(file)
reminder_times = config['reminder_times']

def send_drink_water_reminder():
    """發送喝水提醒到 LINE Notify"""
    message = "🚰 喝水時間到！\n請記得喝一杯水，保持身體健康。"
    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {'message': message}

    try:
        response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)
        response.raise_for_status()  # 檢查 HTTP 錯誤
        logger.info("喝水提醒發送成功！")
    except requests.exceptions.RequestException as e:
        logger.error(f"喝水提醒發送失敗，錯誤: {e}")

# 設定根據配置文件中的時間點發送提醒
for reminder_time in reminder_times:
    schedule.every().day.at(reminder_time).do(send_drink_water_reminder)

# 持續運行任務
while True:
    schedule.run_pending()
    time.sleep(60)  # 等待60秒再檢查
