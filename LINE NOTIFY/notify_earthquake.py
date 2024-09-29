import requests
import os
import time
import hashlib
import json
from dotenv import load_dotenv
from datetime import datetime

# 載入 .env 檔案中的環境變數
load_dotenv('line notify.env')

# 取得 LINE Notify 的 Access Token 和地震 API 的 URL
LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')
EARTHQUAKE_URL = os.getenv('EARTHQUAKE_URL')
LINE_NOTIFY_API_URL = 'https://notify-api.line.me/api/notify'

# 用來存儲已發送的地震事件哈希值
sent_earthquake_hashes = set()

def hash_earthquake_data(eq_info):
    """將地震事件資訊生成唯一的哈希值"""
    eq_str = json.dumps(eq_info, sort_keys=True)
    return hashlib.md5(eq_str.encode('utf-8')).hexdigest()

def send_line_notify(message, image_url=None):
    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'message': message
    }
    if image_url:
        payload['imageThumbnail'] = image_url
        payload['imageFullsize'] = image_url
    response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)
    if response.status_code == 200:
        print(f'Notification sent successfully: {response.status_code}')
    else:
        print(f'Failed to send notification: {response.status_code}, {response.text}')

def check_earthquake():
    try:
        response = requests.get(EARTHQUAKE_URL)
        response.raise_for_status()  # 確保請求成功
        data_json = response.json()
        
        eq_records = data_json.get('records', {}).get('Earthquake', [])
        if not eq_records:
            print("No earthquake records found.")
            return

        for i in eq_records:
            eq_info = i['EarthquakeInfo']
            eq_hash = hash_earthquake_data(eq_info)  # 生成地震事件的哈希值
            magnitude = eq_info['EarthquakeMagnitude']['MagnitudeValue']
            loc = eq_info['Epicenter']['Location']
            dep = eq_info['FocalDepth']
            # 使用 'OriginTime' 作為發生時間
            eq_time = eq_info.get('OriginTime', 'Unknown time')
            # 格式化時間
            try:
                eq_time = datetime.strptime(eq_time, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass  # 如果時間格式無法解析，保持原始格式
            img = i.get('ReportImageURI')
            
            # 只發送芮氏規模大於或等於 4.0 的地震
            if magnitude >= 4.0 and eq_hash not in sent_earthquake_hashes:
                # 組織 msg 訊息
                msg = f'\n{loc}，芮氏規模 {magnitude} 級，深度 {dep} 公里，發生時間 {eq_time}'
                print(msg)
                
                send_line_notify(msg, image_url=img)
                
                # 記錄已發送的地震事件哈希值
                sent_earthquake_hashes.add(eq_hash)

    except requests.RequestException as e:
        print(f'Error fetching earthquake data: {e}')
    except KeyError as e:
        print(f'Error processing data: Missing key {e}')

if __name__ == '__main__':
    while True:
        check_earthquake()
        time.sleep(300)  # 每 5 分鐘檢查一次
