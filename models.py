from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///RapidNews.db")
con = engine.connect()
metaData = Base.metadata
metaData.bind = engine


class User(Base):
	__tablename__ = "User"
	id = Column("id", Integer, primary_key=True)
	leftPeriodBorder = Column("leftPeriodBorder", Integer)
	rightPeriodBorder = Column("rightPeriodBorder", Integer)


class Topic(Base):
	__tablename__ = "Topic"
	id = Column("id", Integer, primary_key=True, autoincrement=True)
	topic = Column("topic", String)


class News(Base):
	__tablename__ = "News"
	id = Column("id", Integer, primary_key=True, autoincrement=True)
	topic = Column("topic", Integer, ForeignKey('Topic.id'))
	title = Column("title", String)
	article = Column("article", String)
	published = Column("published", String)
	url = Column("url", String)


class UserAndTopic(Base):
	__tablename__ = "UserAndTopic"
	id = Column("id", Integer, primary_key=True, autoincrement=True)
	user = Column("user", Integer, ForeignKey('User.id'))
	topic = Column("topic", Integer, ForeignKey('Topic.id'))
	lastSent = Column("lastSent", String)


# metaData.create_all(engine)

