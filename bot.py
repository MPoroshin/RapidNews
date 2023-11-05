import re
from datetime import datetime
import logging
import sys
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import json
from sqlalchemy import join
from sqlalchemy.orm import sessionmaker

from models import User, UserAndTopic, Topic, engine
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
        bot = Bot(token)
        form_router = Router()
        dp = Dispatcher()
        dp.include_router(form_router)
        Session = sessionmaker(bind=engine)
        session = Session()

    @staticmethod
    def checkExistenceOrAddUserInDataBase(userId):
        user = RapidNewsBot.session.query(User).filter(User.id.contains(userId)).first()
        if user is None:
            RapidNewsBot.session.add(
                User(id=userId)
            )
            RapidNewsBot.session.commit()

    @staticmethod
    @form_router.message(CommandStart())
    async def startCommand(message: Message) -> None:
        userId = message.from_user.id
        RapidNewsBot.checkExistenceOrAddUserInDataBase(userId)
        startMessage = RapidNewsBot.jsonBotConfig["messages"]["startMessage"]
        await RapidNewsBot.bot.send_message(userId, startMessage,
                                            reply_markup=ReplyKeyboardRemove())

    """@staticmethod
    @form_router.message(Command("help"))
    async def helpCommand(message: types.Message) -> None:
        userId = message.from_user.id
        allCommandsMessage = RapidNewsBot.jsonBotConfig["messages"]["allCommandsMessage"]
        await RapidNewsBot.bot.send_message(userId, allCommandsMessage,
                                            reply_markup=ReplyKeyboardRemove())"""

    @staticmethod
    @form_router.message(Command("add_topic"))
    async def addTopicCommand(message: types.Message, state: FSMContext) -> None:
        userId = message.from_user.id
        topics = RapidNewsBot.session.query(Topic).all()
        await state.set_state(Form.addTopic)
        await RapidNewsBot.bot.send_message(
            userId,
            RapidNewsBot.jsonBotConfig["messages"]["answerToTypeTopicToAdd"],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=topic.topic)] for topic in topics],
                resize_keyboard=True,
            )
        )

    @staticmethod
    @form_router.message(Form.addTopic)
    async def addTopicProcess(message: Message, state: FSMContext) -> None:
        await state.clear()
        userId = message.from_user.id
        topics = [topic.topic for topic in RapidNewsBot.session.query(Topic).all()]
        topicToBeAdded = message.text
        if topicToBeAdded in topics:
            listOfTopicOfUser = [
                topic.topic for topic in RapidNewsBot.session.query(Topic).select_from(
                    join(UserAndTopic, Topic)
                ).filter(UserAndTopic.user == userId).all()
            ]
            if topicToBeAdded not in listOfTopicOfUser:
                topicId = RapidNewsBot.session.query(Topic).filter(Topic.topic.contains(topicToBeAdded)).first().id
                RapidNewsBot.session.add(UserAndTopic(
                    user=userId,
                    topic=topicId,
                    lastSent=datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
                ))
                RapidNewsBot.session.commit()
                await RapidNewsBot.bot.send_message(
                    userId,
                    RapidNewsBot.jsonBotConfig["messages"]["topicHasBeenAdded"],
                    reply_markup=ReplyKeyboardRemove()
                )
            else:
                await RapidNewsBot.bot.send_message(
                    userId,
                    RapidNewsBot.jsonBotConfig["messages"]["topicHasBeenAddedEarlier"],
                    reply_markup=ReplyKeyboardRemove()
                )
        else:
            await RapidNewsBot.bot.send_message(
                userId,
                RapidNewsBot.jsonBotConfig["messages"]["topicHasBeenTypedNotCorrectly"],
                reply_markup=ReplyKeyboardRemove()
            )

    @staticmethod
    @form_router.message(Command("delete_topic"))
    async def deleteTopicCommand(message: types.Message, state: FSMContext) -> None:
        topics = RapidNewsBot.session.query(Topic).all()
        userId = message.from_user.id
        await state.set_state(Form.deleteTopic)
        await RapidNewsBot.bot.send_message(
            userId,
            RapidNewsBot.jsonBotConfig["messages"]["answerToTypeTopicToDelete"],
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=topic.topic)] for topic in topics],
                resize_keyboard=True,
            ),
        )

    @staticmethod
    @form_router.message(Form.deleteTopic)
    async def deleteTopicProcess(message: Message, state: FSMContext) -> None:
        await state.clear()
        userId = message.from_user.id
        topics = [topic.topic for topic in RapidNewsBot.session.query(Topic).all()]
        topicToBeDeleted = message.text
        if topicToBeDeleted in topics:
            listOfTopicOfUser = [
                topic.topic for topic in RapidNewsBot.session.query(Topic).select_from(
                    join(UserAndTopic, Topic)
                ).filter(UserAndTopic.user == userId).all()
            ]
            if topicToBeDeleted in listOfTopicOfUser:
                topicId = RapidNewsBot.session.query(Topic).filter(Topic.topic.contains(topicToBeDeleted)).first().id
                RapidNewsBot.session.query(UserAndTopic).filter(
                    UserAndTopic.user == userId,
                    UserAndTopic.topic == topicId
                ).delete()
                RapidNewsBot.session.commit()
                await RapidNewsBot.bot.send_message(
                    userId,
                    RapidNewsBot.jsonBotConfig["messages"]["topicHasBeenDeleted"],
                    reply_markup=ReplyKeyboardRemove()
                )
            else:
                await RapidNewsBot.bot.send_message(
                    userId,
                    RapidNewsBot.jsonBotConfig["messages"]["topicHasBeenDeletedEarlier"],
                    reply_markup=ReplyKeyboardRemove()
                )
        else:
            await RapidNewsBot.bot.send_message(
                userId,
                RapidNewsBot.jsonBotConfig["messages"]["topicHasBeenTypedNotCorrectly"],
                reply_markup=ReplyKeyboardRemove()
            )

    @staticmethod
    @form_router.message(Command("change_time"))
    async def changeTimeCommand(message: types.Message, state: FSMContext) -> None:
        userId = message.from_user.id
        await state.set_state(Form.changeTime)
        await RapidNewsBot.bot.send_message(
            userId,
            RapidNewsBot.jsonBotConfig["messages"]["answerToTypeTimeBorder"],
            reply_markup=ReplyKeyboardRemove()
        )

    @staticmethod
    @form_router.message(Form.changeTime)
    async def changeTimeProcess(message: Message, state: FSMContext) -> None:
        await state.clear()
        userId = message.from_user.id
        periodBorders = message.text
        if re.match(r"^(\d\d?)-(\d\d?)$", periodBorders):
            leftPeriodBorder, rightPeriodBorder = map(int, periodBorders.split("-"))
            if (0 <= leftPeriodBorder < 24) and\
                (0 <= rightPeriodBorder < 24) and\
                    (leftPeriodBorder < rightPeriodBorder):
                RapidNewsBot.session.query(User).filter(
                    User.id.contains(userId)).update(
                    {
                        User.leftPeriodBorder: leftPeriodBorder,
                        User.rightPeriodBorder: rightPeriodBorder
                    }, synchronize_session=False)
                RapidNewsBot.session.commit()
                await RapidNewsBot.bot.send_message(
                    userId,
                    RapidNewsBot.jsonBotConfig["messages"]["timeBorderHasBeenChanged"],
                    reply_markup=ReplyKeyboardRemove()
                )
            else:
                await RapidNewsBot.bot.send_message(
                    userId,
                    RapidNewsBot.jsonBotConfig["messages"]["timePeriodIsNotValid"],
                    reply_markup=ReplyKeyboardRemove()
                )
        else:
            await RapidNewsBot.bot.send_message(
                userId,
                RapidNewsBot.jsonBotConfig["messages"]["timePeriodIsNotValid"],
                reply_markup=ReplyKeyboardRemove()
            )

    @staticmethod
    async def main() -> None:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        await RapidNewsBot.dp.start_polling(RapidNewsBot.bot)


