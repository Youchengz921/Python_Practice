import requests

# 發送請求到氣象局 API
url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-B0046-001?Authorization=CWA-6BCF1DAC-DDD6-4339-A895-0F120C91ED4D&downloadType=WEB&format=JSON"
response = requests.get(url)

# 確認請求是否成功
if response.status_code == 200:
    # 解析 JSON 資料
    data = response.json()
    
    # 取得降水預報內容 (降水值以逗號分隔的浮點數列表)
    content = data['cwaopendata']['dataset']['contents']['content']
    precipitation_values = content.split(',')
    
    # 將無效數據轉換為 None
    precipitation_values = [None if value == '-9.900E+01' else float(value) for value in precipitation_values]
    
    # 計算每個格點的經緯度
    start_longitude = 117.975
    start_latitude = 19.975
    grid_resolution = 0.0125
    grid_dimension_x = 441
    grid_dimension_y = 561

    # 初始化空的列表來存儲降水資料
    all_precipitation = []
    
    # 獲取所有有效的降水資料
    for y in range(grid_dimension_y):
        for x in range(grid_dimension_x):
            # 計算當前格點的經緯度
            longitude = start_longitude + x * grid_resolution
            latitude = start_latitude + y * grid_resolution
            index = y * grid_dimension_x + x
            precipitation = precipitation_values[index]
            
            if precipitation is not None and precipitation != -99:
                all_precipitation.append((latitude, longitude, precipitation))

    # 顯示所有有效的降水資料
    if all_precipitation:
        print("所有有效的降水資料:")
        for data in all_precipitation[:10]:  # 僅顯示前 10 條數據作為示例
            print(f"經度: {data[1]}, 緯度: {data[0]}, 降水量: {data[2]} mm")
    else:
        print("沒有有效的降水預報資料")
else:
    print(f"無法獲取資料，狀態碼: {response.status_code}")
