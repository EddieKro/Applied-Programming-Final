import json
import os

from telegram.ext import Dispatcher
from telegram.ext import MessageHandler, Filters
from telegram import Update, Bot, Document
import boto3

def echo(update, context):
    print(update)
    print(context)
    print(update.message.document.file_id)
    doc = Document(file_id=update.message.document.file_id, bot=bot)
    ba = bytes(doc.get_file().download_as_bytearray())
    response = client.put_object(Body=ba, Bucket=os.getenv('DICOM_Bucket'), Key=f'{update._effective_user.id}/{update.message.document.file_name}')
    context.bot.send_message(chat_id=update.effective_chat.id, text='cool, u have sent me a dcm')

bot = Bot(token=os.getenv('TOKEN'))
dispatcher = Dispatcher(bot, None, use_context=True)
echo_handler = MessageHandler(Filters.document.mime_type('application/dicom'), echo)
dispatcher.add_handler(echo_handler)

client = boto3.client('s3')

def handler(event, context):
    dispatcher.process_update(
        Update.de_json(json.loads(event['body']), bot)
    )
    return {"statusCode": 200}
