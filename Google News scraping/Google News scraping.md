爬取Google News資訊
===

模組: scraparazzie
---

```python
from scraparazzie import scraparazzie
```

---

初始化物件
---

**物件 = scraparazzie.NewsClient(參數1, 參數2, ...)**
scraparazzie的參數:

* language: 設定語言，預設en
* location: 設定地區，預設US
* topic: 設定新聞主題
* query: 設定新聞包含的文字
* max_results: 爬取數量，預設: 5，最大: 100

---
**物件.print_news()**
顯示爬取資料，包含標題、連結、來源機構及發布時間。
