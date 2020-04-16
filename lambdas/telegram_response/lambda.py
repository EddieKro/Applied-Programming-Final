import json
import os
import requests

from telegram.ext import Dispatcher
from telegram.ext import MessageHandler, Filters
from telegram import Update, Bot, Document
import boto3
import numpy as np

bot = Bot(token=os.getenv('TOKEN'))

GIFS ={'COVID':[
'https://media.giphy.com/media/3oEduS7uQHMcdiUxA4/giphy.gif',
'https://media.giphy.com/media/Ur7QJQPVtuluAGEBTK/giphy.gif',
'https://media.giphy.com/media/ZcxCeIs3cBYrjKITs1/giphy.gif'],

'NON_COVID':['https://media.giphy.com/media/3oz8xRF0v9WMAUVLNK/giphy.gif',
'https://media.giphy.com/media/qjfeT5XdAirCg/giphy.gif',
'https://media.giphy.com/media/OcZp0maz6ALok/giphy.gif']}

def handler(event, context):
    i = np.random.randint(0,3)

    body = event['body']
<<<<<<< HEAD
    body = json.loads(body)
    bot.send_message(chat_id=body['chat_id'], text=body['message'])
=======
    bot.send_message(chat_id=body['chat_id'], text=body['text'])

    pred=round(body['preds'])

    key = 'COVID' if pred==1 else 'NON_COVID'
    bot.send_animation(chat_id=body['chat_id'], animation=GIFS[key][i])
>>>>>>> 96cd8f09e26ef8e1903169ca3e73a2f48c187faf
    return {"statusCode": 200}
