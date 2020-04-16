import json
import os
import requests

from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Dispatcher
from telegram.ext import CommandHandler,MessageHandler, Filters,CallbackQueryHandler,ConversationHandler
from telegram import Update, Bot, Document
import boto3
import numpy as np
symptoms_ml_url = os.getenv('SYMPTOMS_ML_URL')


#####flask request is sent @line110
#CONVERSATIONAL HANDLER 

INITIAL_INDICES = {'Symptoms':0,'Gender':11,'Age':16,'Contact':21}
AGE_RANGE = ['0-9','10-19','20-24','25-59','59-200']
SYMPTOMS_LIST = ['Fever', 'Tiredness','Dry cough','Sore throat','Difficulty in breath','Pains','Nasal congestion','Running Nose','Diarrhea'] 
SYMPTOMS,GENDER, AGE, CONTACT = range(4)

def start_handler(update, context):
    reply_text="Let's start. What's your name?\n"
    update.message.reply_text(reply_text,reply_markup = ReplyKeyboardRemove())
    return SYMPTOMS


def symptoms_handler(update,context):
    reply_text = "Are you experiencing this particular symptom right now? : "
    reply_keyboard = [['Yes','No']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True)
    
    i = 9-len(SYMPTOMS_LIST)
    print(SYMPTOMS_LIST,i)
    text = update.message.text
    
    if context.user_data and 'Name' in context.user_data.keys():
        if text.lower()=='yes':
            print('answered yes')
            context.user_data['symptoms'].append(i-1)#indices to insert '1'          
    else:
        context.user_data['Name'] = text
        print('username set')
        context.user_data['symptoms']=list()
        print('empty symptoms array set')
    if SYMPTOMS_LIST:
        update.message.reply_text(reply_text+SYMPTOMS_LIST.pop(0),reply_markup=reply_markup)
        return SYMPTOMS
        
    reply_text_G = "What's your gender?"
    reply_keyboard_G = [['Female', 'Male']]
    reply_markup_G=ReplyKeyboardMarkup(reply_keyboard_G,one_time_keyboard=True)    
    update.message.reply_text(reply_text_G,reply_markup=reply_markup_G)
    return GENDER

def gender_handler(update,context):
    gender = update.message.text[0].lower()
    if gender in ['m','f']:
        context.user_data['Gender'] = gender
    else:
        reply_msg = 'Please, input correct gender'
        update.message.reply_text(reply_msg,reply_markup=ReplyKeyboardRemove())
        return GENDER
    
    reply_text = "What's your age group?"
    reply_keyboard = [AGE_RANGE]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True)
    update.message.reply_text(reply_text,reply_markup=reply_markup)
    
    return AGE

        
def age_handler(update,context):
    age,valid,txt = update.message.text,False,str()
    
    if age in AGE_RANGE:
        print(age)
        age = process_age_group(age)
        context.user_data['Age']=age
    else:
        try:
            age = int(age)
            if 0<=age and age<=200:
                valid = True
                context.user_data['Age']=process_age(age)
        except ValueError:
            txt = 'Age must be convertible to int'
    
        if not valid:
            reply_text = 'Please, input correct age. '
            update.message.reply_text(reply_text+txt)
            return AGE
      
    reply_text = 'Did you contact anyone with a virus lately?'
    reply_keyboard = [['Not sure', 'No', 'Yes']]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True)
    update.message.reply_text(reply_text,reply_markup=reply_markup)
    
    return CONTACT

def conctact_handler(update,context):
    contact = update.message.text
    context.user_data['Contact']=process_contact(contact)
    
    symptoms_list = process_data(context.user_data)
    
    chat_id = update.effective_chat.id
    request = {'symptoms': symptoms_list.tolist(), 'chat_id':chat_id}
    update.message.reply_text('Thank you',reply_markup=ReplyKeyboardRemove())
    r = requests.post( url = symptoms_ml_url, json = request)
    return ConversationHandler.END
    
def process_age(age):
    if age<10:
        return 0
    elif age<20:
        return 1
    elif age<25:
        return 2
    elif age<60:
        return 3
    return 4

def process_age_group(age):
    d = {'0-9':0, '10-19':1,'20-24':2,'25-59':3}
    if age not in d.keys():
        return 4
    
def process_contact(contact):
    d = {'yes':2,'no':1}
    if contact in d.keys():
        return d[contact]
    return 0

    
def process_data(user_data):
    symptoms_list = np.zeros((24,),dtype=int)
    for i in user_data['symptoms']:#set first 10
        if i>4:
            i+=1
        symptoms_list[i]=1
    if user_data['Gender']=='f':#set gender
        symptoms_list[INITIAL_INDICES['Gender']]=1
    else:
        symptoms_list[INITIAL_INDICES['Gender']+1]=1
    
    symptoms_list[INITIAL_INDICES['Age']+user_data['Age']]=1#set age
    symptoms_list[INITIAL_INDICES['Contact']+user_data['Contact']]=1#set contacts
    
    if np.all(symptoms_list[:5]==0):#set other
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
  
    return symptoms_list

def echo_handler(update, context):
    msg_text = update.message.text
    update.message.reply_text(text=msg_text,reply_markup=ReplyKeyboardRemove())

    
def cancel_handler(update,context):
    print('cancel')
    update.message.reply_text('Aborting. To restart, press /symptoms', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END



def start(update, context):
    reply_text = "Hello, \n List of commands:\n\t/symptoms -- answer a few questions to understand whether or not you should get to the doctor\n\txray -- upload a .jpg image of your xray to understand whether or not your lungs are infected"
    update.message.reply_text(reply_text,reply_markup=ReplyKeyboardRemove())
    
def _help(update,context):
    help_text = "to start xray check simply upload your .jpeg image or select /xray\nto check your symptoms, use /symptoms"
    update.message.reply_text(help_text,reply_markup=ReplyKeyboardRemove())
    

    
bot = Bot(token=os.getenv('TOKEN'))
dispatcher = Dispatcher(bot, None, use_context=True)


#command handlers
dispatcher.add_handler(CommandHandler('start',start))
dispatcher.add_handler(CommandHandler('xray',echo))
dispatcher.add_handler(CommandHandler('help',_help))
#keyboard handler
dispatcher.add_handler(CallbackQueryHandler(callback = keyboard_callback_handler)

#conversational handler        
conv_handler = ConversationHandler(
    entry_points = [CommandHandler('symptoms',start_handler)],
    states = {
        SYMPTOMS:[
            MessageHandler(Filters.text, symptoms_handler, pass_user_data=True),],
        GENDER:[
            MessageHandler(Filters.text,gender_handler,pass_user_data=True),],
        AGE:[
            MessageHandler(Filters.text,age_handler,pass_user_data=True),],
        CONTACT:[
            MessageHandler(Filters.text,conctact_handler,pass_user_data=True),]
    },
    fallbacks = [CommandHandler('cancel',cancel_handler),])    
dispatcher.add_handler(conv_handler) 

          
def handler(event, context):
    dispatcher.process_update(
        Update.de_json(json.loads(event['body']), bot)
    )
    return {"statusCode": 200}

