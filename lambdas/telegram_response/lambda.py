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
    bot.send_message(body.chat_id, body.text)
    return {"statusCode": 200}
