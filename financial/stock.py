import twstock

# 輸入四位數的股票代碼
while True:
    num = input("請輸入四位數的股票代碼: ")
    
    # 檢查輸入是否為四個數字
    if num.isdigit() and len(num) == 4:
        break
    else:
        print("輸入錯誤，請重新輸入四位數的股票代碼。")

# 使用變數 num 查詢股票資訊
stock = twstock.Stock(num)

# 顯示出現天數
day = int(input("請輸入顯示前幾天的資訊: "))

# 顯示股票資訊
print("日期", stock.date[-day])
print("開盤價", stock.open[-day])
print("最高價", stock.high[-day])
print("最低價", stock.low[-day])
print("關盤價", stock.close[-day])
print("漲跌差", stock.change[-day])
