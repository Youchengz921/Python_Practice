from scraparazzie import scraparazzie

client = scraparazzie.NewsClient(language='chinese traditional', location='Taiwan', topic='Business', max_results=5)

# client.print_news()

items = client.export_news()
print(len(items))

for i, item in enumerate(items):
    print("第" + str(i + 1) + "則新聞")
    print("新聞標題: " + item['title'])
    print("新聞機構: " + item['source'])
    print("新聞連結: " + item['link'])
    print("新聞時間: " + item['publish_date'])
    print("==============================================================")