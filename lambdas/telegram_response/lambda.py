import json
import os
import requests

from telegram.ext import Dispatcher
from telegram.ext import MessageHandler, Filters
from telegram import Update, Bot, Document
import boto3

bot = Bot(token=os.getenv('TOKEN'))

def handler(event, context):
    body = event['body']
    body = json.loads(body)
    bot.send_message(chat_id=body['chat_id'], text=body['message'])
    return {"statusCode": 200}
