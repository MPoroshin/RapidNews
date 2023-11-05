from sqlalchemy.orm import sessionmaker
from models import News, Topic, engine
from NewsParser import Parser, TopicsOfNewsEnum


Session = sessionmaker(bind=engine)
session = Session()


async def loadNews():
	news = {}
	for topic in TopicsOfNewsEnum:
		parser = Parser(topic)
		news[topic.value] = parser.getNews()
	for topic in news.keys():
		newsOnTheTopic = news.get(topic)
		if newsOnTheTopic is not None:
			for dataset in newsOnTheTopic:
				topicRecord = session.query(Topic).filter(Topic.topic.contains(topic)).first()
				session.add(
					News(
						topic=topicRecord.id,
						title=dataset["title"],
						article=dataset["article"],
						published=dataset["published"],
						url=dataset["link"]
					)
				)
	session.commit()
"""

session.add(Topic(topic='World'))
session.add(Topic(topic='Moscow'))
session.add(Topic(topic='Politics'))
session.add(Topic(topic='Society'))
session.add(Topic(topic='Incidents'))
session.add(Topic(topic='ScienceAndTechnology'))
session.add(Topic(topic='ShowBusiness'))
session.add(Topic(topic='Military'))
session.add(Topic(topic='Games'))
session.add(Topic(topic='Analytics'))
session.commit()

"""
