import json
import os
from telegram.ext import Dispatcher
from telegram.ext import MessageHandler, Filters
from telegram import Update, Bot


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

bot = Bot(token=os.getenv('TOKEN'))
dispatcher = Dispatcher(bot, None, use_context=True)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def handler(event, context):
    dispatcher.process_update(
        Update.de_json(json.loads(event['body']), bot)
    )
    return {"statusCode": 200}
