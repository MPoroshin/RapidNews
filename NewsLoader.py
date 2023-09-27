from sqlalchemy import create_engine
import time
from NewsParser import Parser, TopicsOfNewsEnum
from datetime import datetime
import multiprocessing


engine = create_engine("postgresql+psycopg2://postgres:admin@localhost/NewsBot")
engine.connect()




parserSocietyNews = Parser(TopicsOfNewsEnum.SOCIETY_NEWS)
parserEconomicsNews = Parser(TopicsOfNewsEnum.ECONOMICS_NEWS)
parserPoliticsNews = Parser(TopicsOfNewsEnum.POLITICS_NEWS)
parserIncidentNews = Parser(TopicsOfNewsEnum.INCIDENT_NEWS)
parserSportNews = Parser(TopicsOfNewsEnum.SPORT_NEWS)

parserSportNews.getNews()
#абоба


