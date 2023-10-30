import feedparser


World = feedparser.parse("https://news.rambler.ru/rss/world/")
Moscow = feedparser.parse("https://news.rambler.ru/rss/moscow_city/")
Politics = feedparser.parse("https://news.rambler.ru/rss/politics/")
Society = feedparser.parse("https://news.rambler.ru/rss/community/")
Incidents = feedparser.parse("https://news.rambler.ru/rss/incidents/")
ScienceAndTechnology = feedparser.parse("https://news.rambler.ru/rss/tech/")
ShowBusiness = feedparser.parse("https://news.rambler.ru/rss/starlife/")
Military = feedparser.parse("https://news.rambler.ru/rss/army/")
Games = feedparser.parse("https://news.rambler.ru/rss/games/")
Analytics = feedparser.parse("https://news.rambler.ru/rss/articles/")


print(
	World["entries"][0]["link"],
	World["entries"][0]["title"],
	World["entries"][0]["published"],
)
print(
	Moscow["entries"][0]["link"],
	Moscow["entries"][0]["title"],
	Moscow["entries"][0]["published"],
)

print(
	Politics["entries"][0]["link"],
	Politics["entries"][0]["title"],
	Politics["entries"][0]["published"],
)
print(
	Society["entries"][0]["link"],
	Society["entries"][0]["title"],
	Society["entries"][0]["published"],
)
print(
	Incidents["entries"][0]["link"],
	Incidents["entries"][0]["title"],
	Incidents["entries"][0]["published"],
)
print(
	ScienceAndTechnology["entries"][0]["link"],
	ScienceAndTechnology["entries"][0]["title"],
	ScienceAndTechnology["entries"][0]["published"],
)
print(
	ShowBusiness["entries"][0]["link"],
	ShowBusiness["entries"][0]["title"],
	ShowBusiness["entries"][0]["published"],
)
print(
	Military["entries"][0]["link"],
	Military["entries"][0]["title"],
	Military["entries"][0]["published"],
)
print(
	Games["entries"][0]["link"],
	Games["entries"][0]["title"],
	Games["entries"][0]["published"],
)
print(
	Analytics["entries"][0]["link"],
	Analytics["entries"][0]["title"],
	Analytics["entries"][0]["published"],
)