import requests
import schedule
import time
import os
from dotenv import load_dotenv
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta

# 載入 .env 檔案
load_dotenv('line notify.env')

# 取得 LINE Notify API Token
Chose_API = input('1:個人訊息\n2:群組訊息\n:')

if Chose_API == '1':    
    LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')      # 個人TOKEN
    print('已使用個人月經token')
elif Chose_API == '2':
    LINE_NOTIFY_TOKEN = os.getenv('GROUP_TOKEN')        # 群組TOKEN
    print('已使用群組月經token')

LINE_NOTIFY_API_URL = 'https://notify-api.line.me/api/notify'

# 設定日誌檔案處理器
log_dir = 'D:/vscode_python/python bible/LINE NOTIFY/daily_period'
os.makedirs(log_dir, exist_ok=True)  # 確保日誌目錄存在
log_file = os.path.join(log_dir, 'Menstrual_reminder.log')

logger = logging.getLogger('MenstrualReminder')
logger.setLevel(logging.INFO)

# 建立時間滾動日誌處理器，每天新建一個日誌檔案，保存30天的日誌
handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 也將日誌輸出到控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 設定上一次月經結束日期
last_period_end_date_input = input("請輸入上一次月經結束日期 (格式: YYYY-MM-DD): ")
try:
    last_period_end_date = datetime.strptime(last_period_end_date_input, '%Y-%m-%d')
except ValueError:
    print('無效的日期格式，請重新運行程序並輸入正確的日期格式')
    exit()

# 計算下一次月經的預計日期和提醒日期
cycle_length = 30  # 週期長度
reminder_start_day = 21  # 提醒開始於週期第21天
reminder_duration = 7  # 提醒持續7天

next_period_start_date = last_period_end_date + timedelta(days=cycle_length)
reminder_start_date = last_period_end_date + timedelta(days=reminder_start_day)

# 第一次提醒基本訊息
def send_first_message():
    """發送第一次的提示訊息到 LINE Notify"""
    first_msg = (
        f"\n📅 上次結束日期: {last_period_end_date_input}\n"
        f"🔮 下次預計日期是: {next_period_start_date.strftime('%Y-%m-%d')}\n"
        f"⏰ 下次提醒時間是: {reminder_start_date.strftime('%Y-%m-%d')} "
    )

    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {'message': first_msg}
    
    logger.debug(f"正在發送請求到: {LINE_NOTIFY_API_URL}")
    logger.debug(f"發送的標頭: {headers}")
    logger.debug(f"發送的資料: {payload}")

    try:
        response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)
        response.raise_for_status()  # 檢查 HTTP 錯誤
        logger.info("第一次提醒訊息發送成功！")
    except requests.exceptions.RequestException as e:
        logger.error(f"第一次提醒訊息發送失敗，錯誤: {e}", exc_info=True)
        if response is not None:
            logger.error(f"HTTP 狀態碼: {response.status_code}, 響應內容: {response.text}")
        else:
            logger.error("沒有收到響應內容")
            
# 主要提醒訊息
def send_menstrual_reminder():
    """發送月經提醒到 LINE Notify"""
    today = datetime.now().date()
    if reminder_start_date.date() <= today <= (reminder_start_date + timedelta(days=reminder_duration)).date():
        message = "🌸 嘿嘿，小提醒～\n你的小紅即將來訪啦！\n別忘了準備好其他物品喔 💪😌"
        headers = {
            'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {'message': message}

        try:
            response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)
            response.raise_for_status()  # 檢查 HTTP 錯誤
            logger.info(f"月經提醒發送成功！於: {datetime.now()}")
        except requests.exceptions.RequestException as e:
            logger.error(f"月經提醒發送失敗，錯誤: {e}")
    else:
        logger.info(f"今天 {today} 不在提醒範圍內 ({reminder_start_date.strftime('%Y-%m-%d')} - {(reminder_start_date + timedelta(days=reminder_duration)).strftime('%Y-%m-%d')}), 無需發送訊息")

# 設置定時任務
def schedule_menstrual_reminders():
    schedule.every().day.at("20:34").do(send_menstrual_reminder)
    logger.info(f"月經提醒已設定，將從 {reminder_start_date.strftime('%Y-%m-%d')} 開始，每天發送提醒共 {reminder_duration} 天")

# 發送第一次訊息
send_first_message()

# 執行提醒設置
schedule_menstrual_reminders()

# 開始運行定時任務
while True:
    schedule.run_pending()
    logger.debug(f"等待執行定時任務，當前時間: {datetime.now()}")
    time.sleep(60)  # 每分鐘檢查一次
