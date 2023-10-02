import re
import html
import feedparser
import time
from datetime import datetime
from random import choice
from bs4 import BeautifulSoup as BS
import requests
from fake_useragent import UserAgent
from enum import Enum
import json
from functools import reduce


class TopicsOfNewsEnum(Enum):
	SPORT_NEWS = 'Sport'
	SOCIETY_NEWS = 'Society'
	INCIDENT_NEWS = 'Incident'
	ECONOMICS_NEWS = 'Economics'
	POLITICS_NEWS = 'Politics'


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
			self.__pathToTitle = self.__jsonParserConfig[f"{self.__topicOfNews.value}"]["pathToTitle"]
			self.__pathToPublished = self.__jsonParserConfig[f"{self.__topicOfNews.value}"]["pathToPublished"]
			self.__pathToPageURL = self.__jsonParserConfig[f"{self.__topicOfNews.value}"]["pathToPageURL"]
			self.__lastUpdate = self.__formatDate(
				self.__jsonParserConfig[f"{self.__topicOfNews.value}"]["lastUpdate"]
			)
			self.__getEntries(self.__rssURL)

	def __getEntries(self, url):
		self.__feed = feedparser.parse(url)["entries"]

	def __getItemFromFeedUsingPath(self, path, index):
		element = self.__feed[index]
		for part in path:
			element = element[part]
		return element

	def __getNews(self, count):
		resultJSON = []
		for index in range(count):
			self.__newsPageURL = self.__getItemFromFeedUsingPath(self.__pathToPageURL, index)
			self.__newsPublished = self.__getItemFromFeedUsingPath(self.__pathToPublished, index)
			self.__newsTitle = self.__getItemFromFeedUsingPath(self.__pathToTitle, index)
			self.__newsArticle = Parser.__getArticleFromURL(self.__newsPageURL)
			resultJSON.append({
				"title": self.__newsTitle,
				"article": self.__newsArticle,
				"link": self.__newsPageURL,
				"published": self.__newsPublished
			})
		return resultJSON

	def __getPublished(self, index):
		self.__newsPublished = self.__getItemFromFeedUsingPath(self.__pathToPublished, index)
		return self.__newsPublished

	@staticmethod
	def __getArticleFromURL(url):
		textHTML = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
		bs = BS(textHTML, 'html.parser')
		allTagsFromHTML = bs.find_all(["p"]) # мега пакость
		article = reduce(lambda a, b: a.text + ' ' + b.text, allTagsFromHTML)
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

	def getNews(self):
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

#абоба