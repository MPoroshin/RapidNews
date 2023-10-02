from sqlalchemy import create_engine
import time
from NewsParser import Parser, TopicsOfNewsEnum
from datetime import datetime
import multiprocessing


engine = create_engine("postgresql+psycopg2://postgres:admin@localhost/NewsBot")
engine.connect()
"""
в с ку лайт есть транзации?
мне нада чтобы новости добавлялись в нескольких потоках каждый поток для отдельной рсс ленты
они одновременно будут изменять таблицу в бд и надо чтобы было нормально
на
"""


parserSocietyNews = Parser(TopicsOfNewsEnum.SOCIETY_NEWS)
parserEconomicsNews = Parser(TopicsOfNewsEnum.ECONOMICS_NEWS)
parserPoliticsNews = Parser(TopicsOfNewsEnum.POLITICS_NEWS)
parserIncidentNews = Parser(TopicsOfNewsEnum.INCIDENT_NEWS)
parserSportNews = Parser(TopicsOfNewsEnum.SPORT_NEWS)


print(parserSocietyNews.getNews())
print(parserEconomicsNews.getNews())
print(parserPoliticsNews.getNews())
print(parserIncidentNews.getNews())
print(parserSportNews.getNews())


