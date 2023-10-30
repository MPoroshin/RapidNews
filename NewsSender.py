from datetime import datetime
from models import User, News, UserAndTopic, Topic, session, con
from sqlalchemy import join

"""
def sendNews():
	currentHour = datetime.now().hour

	session.query(News).select_from(join(News, ))

	con.execute(
		
	
	
	)

	usersAreReadyToReceiveNewsNow = session.query(User).filter(User.id.contains(
		User.leftPeriodBorder <= currentHour,
		User.rightPeriodBorder > currentHour
		)).all()
	for user in usersAreReadyToReceiveNewsNow:

		listOfTopicIdOfUser = [
			topic.id for topic in session.query(Topic).select_from(
				join(UserAndTopic, Topic)
			).filter(UserAndTopic.user == user.id).all()
		]
		listOfNewsToSendToUser = []
		for topic in listOfTopicIdOfUser:
			listOfNewsToSendToUser.append(
				session.query(News).select_from(
					join(News, )
			).filter(UserAndTopic.user == user.id).all()
			)
		listOfNewsToSendToUser = [
			news for news in session.query(News).select_from(
				join(, )
			).filter(UserAndTopic.user == user.id).all()
		]


sendNews()"""