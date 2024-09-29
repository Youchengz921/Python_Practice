import requests
import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv('line notify.env')

# 取得 API Token
LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')      # 個人測試token
# LINE_NOTIFY_TOKEN = os.getenv('GROUP_TOKEN')      # 群組token
WEATHER_API_TOKEN = os.getenv('MYSELF_API')
LINE_NOTIFY_API_URL = 'https://notify-api.line.me/api/notify'

# 定義縣市代碼
city_codes = {
    "1": "臺北市",
    "2": "新北市",
    "3": "桃園市",
    "4": "臺中市",
    "5": "臺南市",
    "6": "高雄市",
    "7": "基隆市",
    "8": "新竹市",
    "9": "新竹縣",
    "10": "苗栗縣",
    "11": "彰化縣",
    "12": "南投縣",
    "13": "雲林縣",
    "14": "嘉義市",
    "15": "嘉義縣",
    "16": "屏東縣",
    "17": "宜蘭縣",
    "18": "花蓮縣",
    "19": "臺東縣",
    "20": "澎湖縣",
    "21": "金門縣",
    "22": "連江縣"
}

# 輸入縣市代碼
print("請選擇縣市代碼查詢天氣：")
for code, city in city_codes.items():
    print(f"{code}: {city}")

city_code = input("輸入代碼: ")

# 根據輸入的代碼取得縣市名稱
city_name = city_codes.get(city_code)

def send_line_notify(message):
    """發送消息到 LINE Notify"""
    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {'message': message}
    response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)
    if response.status_code == 200:
        print("通知發送成功！")
    else:
        print(f"通知發送失敗，狀態碼: {response.status_code}")

if city_name:
    # 使用 city_name 查詢天氣
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={WEATHER_API_TOKEN}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查 HTTP 錯誤

        # 檢查響應內容
        data = response.json()

        # 處理氣象資料
        location_data = next((item for item in data.get("records", {}).get("location", []) if item["locationName"] == city_name), None)
        
        if location_data:
            # 資料提取
            weather_element = {elem['elementName']: elem for elem in location_data.get("weatherElement", [])}
            
            # 提取時間範圍中的日期
            times = weather_element.get("Wx", {}).get("time", [{}])
            if times:
                date_range = f"{times[0].get('startTime', '未知')[:10]} 至 {times[-1].get('endTime', '未知')[:10]}"
            else:
                date_range = "未知"
            
            weather = weather_element.get("Wx", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")
            rain_probability = weather_element.get("PoP", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")
            min_temp = weather_element.get("MinT", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")
            max_temp = weather_element.get("MaxT", {}).get("time", [{}])[0].get("parameter", {}).get("parameterName", "未知")

            # 組織訊息
            message = (f"單一縣市播報\n{city_name}的天氣預報 :\n"
                       f"{date_range} \n"
                       f"天氣狀況: {weather}\n"
                       f"降雨機率: {rain_probability}%\n"
                       f"最高溫度: {max_temp}°C\n"
                       f"最低溫度: {min_temp}°C")
            
            print(message)  # 顯示在控制台
            send_line_notify(message)  # 發送到 LINE Notify
        else:
            print(f"無法取得 {city_name} 的天氣資料。")
    
    except requests.exceptions.RequestException as e:
        print(f"請求發生錯誤: {e}")
    except ValueError as e:
        print(f"JSON 解析錯誤: {e}")
else:
    print("無效的縣市代碼，請重新輸入。")
