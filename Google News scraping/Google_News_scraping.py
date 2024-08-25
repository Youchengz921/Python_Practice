from scraparazzie import scraparazzie

client = scraparazzie.NewsClient(language='chinese traditional', location='Taiwan', topic='Business', max_results=8)

client.print_news()
