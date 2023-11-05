import asyncio
import json
from datetime import datetime as dt, timedelta
from aiogram import Bot
from sqlalchemy.orm import sessionmaker
from models import User, News, UserAndTopic, engine


Session = sessionmaker(bind=engine)
session = Session()
with open('BotConfig.json', 'r', encoding='utf-8') as file:
	jsonBotConfig = json.load(file)
	token = jsonBotConfig["TOKEN"]
	bot = Bot(token)


async def sendNews():
	currentHour = dt.now().hour
	dateFormat = '%a, %d %b %Y %H:%M:%S %z'
	recordsNews = session.query(
		User.id,
		News.title,
		News.article,
		News.published,
		News.url,
		News.topic,
		User.leftPeriodBorder,
		User.rightPeriodBorder
	).filter(
		User.leftPeriodBorder <= currentHour,
		User.rightPeriodBorder > currentHour,
		User.id == UserAndTopic.user,
		News.topic == UserAndTopic.topic,
		News.published > UserAndTopic.lastSent,
	).all()
	for record in recordsNews:
		newsPublished = record[3]
		userLeftPeriodBorder = record[6]
		userRightPeriodBorder = record[7]
		datetime_object = dt.strptime(newsPublished, '%a, %d %b %Y %H:%M:%S %z')
		hour = datetime_object.time().hour
		if userLeftPeriodBorder <= hour < userRightPeriodBorder:
			await asyncio.sleep(1 / 30)
			asyncio.create_task(
				bot.send_message(
					chat_id=record[0],
					text=f"{record[1]}\n{record[2]}\n{record[3]}\n{record[4]}"
				)
			)
		userId = record[0]
		topicId = record[5]
		session.query(UserAndTopic).filter(
			UserAndTopic.user.contains(userId),
			UserAndTopic.topic.contains(topicId)
		).update(
			{
				UserAndTopic.lastSent: newsPublished
			}, synchronize_session=False)
	current_date = dt.now()
	yesterday_date = current_date - timedelta(days=1)
	yesterday_date_str = yesterday_date.strftime('%a, %d %b %Y %H:%M:%S %z')
	session.query(News).filter(
		News.published < yesterday_date_str
	).delete(synchronize_session=False)
	session.commit()

