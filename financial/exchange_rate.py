import twder

# 定義貨幣字典和交易類型列表
currencies = {
    'USD': '美金 ', 'HKD': '港幣 ',
    'GBP': '英鎊 ', 'AUD': '澳幣 ',
    'CAD': '加拿大幣 ', 'SGD': '新加坡幣 ',
    'CHF': '瑞士法郎 ', 'JPY': '日圓 ',
    'ZAR': '南非幣 ', 'SEK': '瑞典幣 ',
    'NZD': '紐元 ', 'THB': '泰幣 ',
    'PHP': '菲國比索 ', 'IDR': '印尼幣 ',
    'EUR': '歐元 ', 'KRW': '韓元 ',
    'VND': '越南盾 ', 'MYR': '馬來幣 ',
    'CNY': '人民幣 '
}
keys = currencies.keys()
tlist = ['現金買入', '現金賣出', '即期買入', '即期賣出']

# 列出所有可選貨幣並提示用戶輸入選擇
print("請選擇以下貨幣的縮寫:")
for key, value in currencies.items():
    print(f"{value}: {key}")

# 接受用戶輸入的貨幣代碼
currency_key = input("輸入貨幣縮寫: ").upper()

# 更新顯示匯率資訊
if currency_key in keys:
    view = currencies[currency_key] + '匯率:\n'
    for i in range(4):
        exchange = twder.now(currency_key)[i + 1]
        view = view + tlist[i] + ': ' + str(exchange) + '\n'
    print(view)
else:
    print("No Information")
