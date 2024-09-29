import requests
import os
import json
from dotenv import load_dotenv
import schedule
import time
import logging

# 獲取程式碼所在目錄
current_directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_directory, 'app.log')

# 刪除舊的 app.log 文件（如果存在）
if os.path.exists(log_file_path):
    os.remove(log_file_path)
    print(f"舊的日誌文件 {log_file_path} 已被刪除。")
else:
    print("沒有找到舊的日誌文件。")

# 設置日誌到文件
logger = logging.getLogger('weather_logger')
logger.setLevel(logging.DEBUG)  # 設定最低記錄級別

# 創建 FileHandler，並設定最大文件大小和備份數量
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)  # 設定 FileHandler 的級別

# 設定日誌格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 將 FileHandler 添加到 Logger
logger.addHandler(file_handler)

# 載入 .env 檔案
# load_dotenv('D:/vscode_python/python bible/LINE NOTIFY/everyday_weather/daily_weather.env')
load_dotenv('line notify.env')

# 取得 API Token 和配置路徑
Chose_API = input('1: 個人\n2: 群組\n:')

if Chose_API == '1': 
    LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')
    print("已使用個人天氣Line Notify。")
elif Chose_API == '2':
    LINE_NOTIFY_TOKEN = os.getenv('GROUP_TOKEN')
    print("已使用群組天氣Line Notify。")
    
WEATHER_API_TOKEN = os.getenv('MYSELF_API')
LINE_NOTIFY_API_URL = 'https://notify-api.line.me/api/notify'
config_path = os.getenv('CONFIG_PATH')

def load_config():
    """讀取配置文件"""
    if not config_path:
        raise ValueError("CONFIG_PATH 未設定")
    
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def send_line_notify(message, retries=3, delay=5):
    """發送消息到 LINE Notify，支持重試機制"""
    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {'message': message}
    for attempt in range(retries):
        try:
            response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)
            response.raise_for_status()  # 檢查 HTTP 錯誤
            logger.info("通知發送成功！")
            break
        except requests.exceptions.RequestException as e:
            logger.error(f"通知發送失敗，錯誤: {e}")
            if attempt < retries - 1:
                logger.info(f"等待 {delay} 秒後重試...")
                time.sleep(delay)  # 等待一段時間再重試
    else:
        logger.error(f"通知發送失敗，錯誤: {e}")

def fetch_weather_and_notify(city_name):
    """查詢天氣並發送到 LINE Notify"""
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={WEATHER_API_TOKEN}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查 HTTP 錯誤

        data = response.json()

        # 處理氣象資料
        location_data = next((item for item in data.get("records", {}).get("location", []) if item["locationName"] == city_name), None)
        
        if location_data:
            weather_element = {elem.get('elementName', '未知'): elem for elem in location_data.get("weatherElement", [])}
            
            times = weather_element.get("Wx", {}).get("time", [])
            if times:
                date_range = f"{times[0].get('startTime', '未知')[:10]} 至 {times[-1].get('endTime', '未知')[:10]}"
            else:
                date_range = "未知"
            
            weather = weather_element.get("Wx", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")
            rain_probability = weather_element.get("PoP", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")
            min_temp = weather_element.get("MinT", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")
            max_temp = weather_element.get("MaxT", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")
            wind_speed = weather_element.get("WDSD", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")
            humidity = weather_element.get("HUMD", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")

            notification_message = ""
            if int(rain_probability) > 50 and int(max_temp) > 30:
                notification_message = "\n☔ 機率超過50%，🔥超過30°C，記得攜帶雨具並注意防暑！"
            elif int(rain_probability) > 50:
                notification_message = "\n☔ 降雨機率超過50%，記得攜帶雨具！"
            elif int(max_temp) > 30:
                notification_message = "\n🔥 高溫超過30°C，請注意防暑！"

            message = (
                f"📣 天氣預報 🚨\n"
                f"地點: 【{city_name}】\n"
                f"日期: {date_range}\n"
                f"🌤 天氣狀況: {weather}\n"
                f"☔ 降雨機率: {rain_probability}%\n"
                f"🌡 最高溫度: {max_temp}°C\n"
                f"🌡 最低溫度: {min_temp}°C"
                f"{notification_message}"
            )
            
            send_line_notify(message)
        else:
            logger.warning(f"無法取得 {city_name} 的天氣資料。")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"請求發生錯誤: {e}")
    except ValueError as e:
        logger.error(f"JSON 解析錯誤: {e}")

def job():
    """每天特定時間執行的任務"""
    try:
        config = load_config()
        cities_to_notify = config.get('cities', [])
        for city in cities_to_notify:
            fetch_weather_and_notify(city)
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"配置文件錯誤: {e}")
        exit(1)

# 設定每天執行任務時間
try:
    config = load_config()
    notify_times = config.get('notify_times', [])
    for notify_time in notify_times:
        schedule.every().day.at(notify_time).do(job)
except (FileNotFoundError, ValueError) as e:
    logger.error(f"配置文件錯誤: {e}")
    exit(1)

while True:
    schedule.run_pending()
    time.sleep(60)  # 等待60秒再檢查
