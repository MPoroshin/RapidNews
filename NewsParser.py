import feedparser
from datetime import datetime
from bs4 import BeautifulSoup as BS
import requests
from fake_useragent import UserAgent
from enum import Enum
import json


class TopicsOfNewsEnum(Enum):
	World = 'World'
	Moscow = 'Moscow'
	Politics = 'Politics'
	Society = 'Society'
	Incidents = 'Incidents'
	ScienceAndTechnology = 'ScienceAndTechnology'
	ShowBusiness = 'ShowBusiness'
	Military = 'Military'
	Games = 'Games'
	Analytics = 'Analytics'


class Parser:
	def __init__(self, topicOfNews: TopicsOfNewsEnum):
		self.__feed = None
		self.__newsPageURL = None
		self.__newsPublished = None
		self.__newsTitle = None
		self.__newsArticle = None
		self.__topicOfNews = topicOfNews
		with open('ParserConfig.json', 'r') as file:
			self.__jsonParserConfig = json.load(file)
			self.__rssURL = self.__jsonParserConfig[f"{self.__topicOfNews.value}"]["rssURL"]
			self.__lastUpdate = self.__formatDate(
				self.__jsonParserConfig[f"{self.__topicOfNews.value}"]["lastUpdate"]
			)
			self.__setEntries(self.__rssURL)

	def __setEntries(self, url):
		self.__feed = feedparser.parse(url)['entries']

	def __getNews(self, count) -> list:
		resultJSON = []
		for index in range(count):
			self.__newsPageURL = self.__getPageURL(index)
			self.__newsPublished = self.__getPublished(index)
			self.__newsTitle = self.__getTitle(index)
			self.__newsArticle = Parser.__getArticleFromURL(self.__newsPageURL)
			resultJSON.append({
				"title": self.__newsTitle,
				"article": self.__newsArticle,
				"link": self.__newsPageURL,
				"published": self.__newsPublished
			})
		return resultJSON

	def __getPublished(self, index) -> str:
		self.__newsPublished = self.__feed[index]['published']
		return self.__newsPublished

	def __getTitle(self, index) -> str:
		self.__newsTitle = self.__feed[index]['title']
		return self.__newsTitle

	def __getPageURL(self, index) -> str:
		self.__newsPageURL = self.__feed[index]['link']
		return self.__newsPageURL

	@staticmethod
	def __getArticleFromURL(url) -> str:
		textHTML = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
		bs = BS(textHTML, 'html.parser')
		allTagsFromHTML = bs.find_all(["p"], {'class': None})
		allTagsFromHTML = [tag.text for tag in allTagsFromHTML]
		article = ' '.join(allTagsFromHTML)
		return article

	@staticmethod
	def __outputArticleToConsole(title, article, published, url):
		print("Заголовок: " + title)
		print("Текст: " + article)
		print("Дата: " + published)
		print("Ссылка:" + url)

	@staticmethod
	def __formatDate(date):
		return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')

	def getNews(self) -> list:
		count = 0
		for index in range(len(self.__feed)):
			newLastUpdate = self.__formatDate(self.__getPublished(index))
			if self.__lastUpdate < newLastUpdate:
				count += 1
			else:
				break

		if count > 0:
			self.__lastUpdate = self.__getPublished(0)
			with open('ParserConfig.json', 'r+') as file:
				parserConfig = json.load(file)
				parserConfig[f"{self.__topicOfNews.value}"]["lastUpdate"] = self.__lastUpdate
				file.seek(0)
				file.truncate()
				json.dump(parserConfig, file)
			return self.__getNews(count)

