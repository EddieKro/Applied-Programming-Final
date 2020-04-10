import json
import os
import requests

from telegram import InlineKeyboardButton,InlineKeyboardMarkup

from telegram.ext import Dispatcher
from telegram.ext import CommandHandler,MessageHandler, Filters,CallbackQueryHandler
from telegram import Update, Bot, Document
import boto3
import numpy as np
ml_url = os.getenv('ML_URL')
symptoms_ml_url = os.getenv('SYMPTOMS_ML_URL')

def get_base_inline_keyboard():
    
    keyboard = [[InlineKeyboardButton("Check COVID Symptoms", callback_data='1'),
                 InlineKeyboardButton("Check XRay image for COVID", callback_data='2')],
               [InlineKeyboardButton("Help", callback_data='3')]]

    return InlineKeyboardMarkup(keyboard)

def start(update, context):
    reply_text = "Hello, \n List of commands:\n\t/symptoms -- answer a few questions to understand whether or not you should get to the doctor\n\txray -- upload a .jpg image of your xray to understand whether or not your lungs are infected"
    reply_markup = get_base_inline_keyboard()
    update.message.reply_text(reply_text,reply_markup=reply_markup)
    
def _help(update,context):
    help_text = "to start xray check simply upload your .jpeg image or select /xray\nto check your symptoms, use /symptoms"
    reply_markup = get_base_inline_keyboard()
    update.message.reply_text(help_text,reply_markup=reply_markup)
    
    
def keyboard_callback_handler(update, context):
    query = update.callback_query
    data = query.data
    
    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text
    
    if data.contains(':'):
        ans,index = data.split(':')
        if ans=='yes':
            symptoms_list[int(index)] = 1
                    
    if data.contains(','):
        block,index = list(map(int,data.split(',')))
        symptoms_list[initial_indices[block]+index] = 1
        
    if data == '1':
        #start symptoms_echo
        symptoms_echo(update,context)
    elif data == '2':
        #start echo
        echo(update,context)
    else:
        #start help
        _help(update,context)
        
    
def form_keyboard(question_block_index,questions):
    keyboard = [[InlineKeyboardButton(questions[i]),callback_data=f'{question_block_index},{i}'] for i in range(len(questions))]
    reply_keyboard_markup = InlineKeyboardMarkup(keyboard)
    return reply_keyboard_markup
        
def form_yes_no_keyboard(i):
    if i==5 or i==10:#special questions
        i+=1
    keyboard = [[InlineKeyboardButton('Yes',callback_data=f'yes:{i}'), InlineKeyboardButton('No',callback_data=f'no:{i}')]]
    reply_keyboard_markup = InlineKeyboardMarkup(keyboard)
    return reply_keyboard_markup
        
def symptoms_echo(update,context):
    symptoms_list = np.zeros((25,),dtype=int)#should be defined globally
    
    for block in question_blocks:
        if block=='symptoms':
            for i in range(len(descriptions[block])):
                reply_text = descriptions[block] + question_blocks['symptoms'][i]
                if i>=5:
                    i+=1
                reply_markup = form_yes_no_keyboard(i)
                update.message.reply_text(reply_text,reply_markup=reply_markup)
        else:
            reply_text = descriptions[block]
            reply_markup = form_keyboard()#todo
            update.message.reply_text(reply_text,reply_markup=reply_markup)            
    
    if np.all(symptoms_list[:5]==0):
        symptoms_list[5]==1
    if np.all(symptoms_list[6:10]==0):
        symptoms_list[10]=1
    
    severity_symps = [symptoms_list[5],symptoms_list[10]]
    if np.all(severity_symps)==1:
        symptoms_list[18]=1
    elif np.all(severity_symps)==0:
        symptoms_list[18]=1
    else:
        symptoms_list[19]=1
        
    
    chat_id = update.effective_chat.id
    request = {'symptoms': symptoms_list.tolist(), 'chat_id':chat_id}
    r = requests.post( url = symptoms_ml_url, json = request)
    

def echo(update, context):
    print(update)
    print(context)
    print(update.message.document.file_id)
    doc = Document(file_id=update.message.document.file_id, bot=bot)
    image_b = np.frombuffer(doc.get_file().download_as_bytearray(),dtype=np.uint8).tolist()
    chat_id = update.effective_chat.id
    request = {'image': image_b, 'chat_id': chat_id}
    r = requests.post( url = ml_url+'/xray/predict', json = request)
    print('r send')
    print(r)
    # response = client.put_object(Body=ba, Bucket=os.getenv('DICOM_Bucket'), Key=f'{update._effective_user.id}/{update.message.document.file_name}')
    # context.bot.send_message(chat_id=update.effective_chat.id, text='cool, u have sent me a dcm')

    
bot = Bot(token=os.getenv('TOKEN'))
dispatcher = Dispatcher(bot, None, use_context=True)
<<<<<<< Updated upstream
echo_handler = MessageHandler(Filters.document.mime_type('image/jpeg'), echo)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(MessageHandler(Filters.document.mime_type('image/pjpeg'), echo))
=======

#Bodya-handler
echo_handler = MessageHandler(Filters.document.mime_type('application/dicom'), echo)
dispatcher.add_handler(echo_handler)


#command handlers
dispatcher.add_handler(CommandHandler('start',start))
dispatcher.add_handler(CommandHandler('symptoms',start))
dispatcher.add_handler(CommandHandler('xray',echo))
dispatcher.add_handler(CommandHandler('help',_help))
#keyboard handler
dispatcher.add_handler(CallbackQueryHandler(callback = keyboard_callback_handler)



>>>>>>> Stashed changes
def handler(event, context):
    dispatcher.process_update(
        Update.de_json(json.loads(event['body']), bot)
    )
    return {"statusCode": 200}

