import asyncio
import re
from datetime import datetime
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
import json

from sqlalchemy import join

from models import User, News, UserAndTopic, Topic, session
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class Form(StatesGroup):
    changeTime = State()
    addTopic = State()
    deleteTopic = State()


class RapidNewsBot:
    with open('BotConfig.json', 'r', encoding='utf-8') as file:
        jsonBotConfig = json.load(file)
        token = jsonBotConfig["TOKEN"]
        bot = Bot(token, parse_mode=ParseMode.HTML)
        form_router = Router()
        dp = Dispatcher()
        dp.include_router(form_router)

    @staticmethod
    def checkExistenceOrAddUserInDataBase(userId):
        user = session.query(User).filter(User.id.contains(userId)).first()
        if user is None:
            session.add(
                User(id=userId)
            )
            session.commit()

    @staticmethod
    @form_router.message(CommandStart())
    async def startCommand(message: Message) -> None:
        userId = message.from_user.id
        RapidNewsBot.checkExistenceOrAddUserInDataBase(userId)
        allCommandsMessage = RapidNewsBot.jsonBotConfig["messages"]["allCommandsMessage"]
        await message.answer(allCommandsMessage)

    @staticmethod
    @form_router.message(Command("help"))
    async def helpCommand(message: types.Message) -> None:
        allCommandsMessage = RapidNewsBot.jsonBotConfig["messages"]["allCommandsMessage"]
        await message.answer(allCommandsMessage)

    @staticmethod
    @form_router.message(Command("add_topic"))
    async def addTopicCommand(message: types.Message, state: FSMContext) -> None:
        topics = session.query(Topic).all()
        await state.set_state(Form.addTopic)
        await message.answer(
            RapidNewsBot.jsonBotConfig["answerToTypeTopicToAdd"],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=topic.topic)] for topic in topics],
                resize_keyboard=True,
            ),
        )

    @staticmethod
    @form_router.message(Form.addTopic)
    async def addTopicProcess(message: Message, state: FSMContext) -> None:
        await state.clear()
        topics = [topic.topic for topic in session.query(Topic).all()]
        topicToBeAdded = message.text
        if topicToBeAdded in topics:
            userId = message.from_user.id
            listOfTopicOfUser = [
                topic.topic for topic in session.query(Topic).select_from(
                    join(UserAndTopic, Topic)
                ).filter(UserAndTopic.user == userId).all()
            ]
            if topicToBeAdded not in listOfTopicOfUser:
                topicId = session.query(Topic).filter(Topic.topic.contains(topicToBeAdded)).first().id
                session.add(UserAndTopic(
                    user=userId,
                    topic=topicId,
                    lastSent=datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
                ))
                session.commit()
                await message.answer(RapidNewsBot.jsonBotConfig["topicHasBeenAdded"],
                                     reply_markup=ReplyKeyboardRemove())
            else:
                await message.answer(RapidNewsBot.jsonBotConfig["topicHasBeenAddedEarlier"],
                                     reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(RapidNewsBot.jsonBotConfig["topicHasBeenTypedNotCorrectly"],
                                 reply_markup=ReplyKeyboardRemove())

    @staticmethod
    @form_router.message(Command("delete_topic"))
    async def deleteTopicCommand(message: types.Message, state: FSMContext) -> None:
        topics = session.query(Topic).all()
        await state.set_state(Form.deleteTopic)
        await message.answer(
            RapidNewsBot.jsonBotConfig["answerToTypeTopicToDelete"],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=topic.topic)] for topic in topics],
                resize_keyboard=True,
            ),
        )

    @staticmethod
    @form_router.message(Form.deleteTopic)
    async def deleteTopicProcess(message: Message, state: FSMContext) -> None:
        await state.clear()
        topics = [topic.topic for topic in session.query(Topic).all()]
        topicToBeDeleted = message.text
        if topicToBeDeleted in topics:
            userId = message.from_user.id
            listOfTopicOfUser = [
                topic.topic for topic in session.query(Topic).select_from(
                    join(UserAndTopic, Topic)
                ).filter(UserAndTopic.user == userId).all()
            ]
            if topicToBeDeleted in listOfTopicOfUser:
                topicId = session.query(Topic).filter(Topic.topic.contains(topicToBeDeleted)).first().id
                session.query(UserAndTopic).filter(
                    UserAndTopic.user == userId,
                    UserAndTopic.topic == topicId
                ).delete()
                session.commit()
                await message.answer(RapidNewsBot.jsonBotConfig["topicHasBeenDeleted"],
                                     reply_markup=ReplyKeyboardRemove())
            else:
                await message.answer(RapidNewsBot.jsonBotConfig["topicHasBeenDeletedEarlier"],
                                     reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(RapidNewsBot.jsonBotConfig["topicHasBeenTypedNotCorrectly"],
                                 reply_markup=ReplyKeyboardRemove())

    @staticmethod
    @form_router.message(Command("change_time"))
    async def changeTimeCommand(message: types.Message, state: FSMContext) -> None:
        await state.set_state(Form.changeTime)
        await message.answer(RapidNewsBot.jsonBotConfig["answerToTypeTimeBorder"],
                             reply_markup=ReplyKeyboardRemove())

    @staticmethod
    @form_router.message(Form.changeTime)
    async def changeTimeProcess(message: Message, state: FSMContext) -> None:
        await state.clear()
        periodBorders = message.text
        if re.match(r"^(\d\d?)-(\d\d?)$", periodBorders):
            leftPeriodBorder, rightPeriodBorder = map(int, periodBorders.split("-"))
            if (0 <= leftPeriodBorder < 24) and\
                (0 <= rightPeriodBorder < 24) and\
                    (leftPeriodBorder < rightPeriodBorder):
                userId = message.from_user.id
                session.query(User).filter(
                    User.id.contains(userId)).update(
                    {
                        User.leftPeriodBorder: leftPeriodBorder,
                        User.rightPeriodBorder: rightPeriodBorder
                    }, synchronize_session=False)
                session.commit()
                await message.answer(RapidNewsBot.jsonBotConfig["timeBorderHasBeenChanged"],
                                     reply_markup=ReplyKeyboardRemove())
            else:
                await message.answer(RapidNewsBot.jsonBotConfig["timePeriodIsNotValid"],
                                     reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(RapidNewsBot.jsonBotConfig["timePeriodIsNotValid"],
                                 reply_markup=ReplyKeyboardRemove())

    @staticmethod
    async def main() -> None:
        await RapidNewsBot.dp.start_polling(RapidNewsBot.bot)


def startBot():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(RapidNewsBot.main())