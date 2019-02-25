#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Initialize the wechat bot
from wxpy import *
bot = Bot()

#Search the wechat friend
my_friend = bot.friends().search('江南')[0]


# In[ ]:





# In[11]:


# Import necessary modules
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

# Create a trainer that uses this config
trainer = Trainer(config.load("config_spacy.yml"))

# Load the training data
training_data = load_data('demo-rasa-noents.json')

# Create an interpreter by training the model
interpreter = trainer.train(training_data)


# In[12]:


#Define policy_rules
INIT = 1

policy_rules={
    (INIT,'greet'):(INIT,1),
    (INIT,'help'):(INIT,1),
    (INIT,'weather_ask'):(INIT,2),
    (INIT,'stock_historical_ask'):(INIT,2),
    (INIT,'weather_continue'):(INIT,3),
    (INIT,'stock_ask'):(INIT,4),
    (INIT,'historical_continue'):(INIT,5),
    (INIT,'weekday_ask'):(INIT,6),
    (INIT,'historical_continue'):(INIT,7),
    (INIT,'goodbye'):(INIT,1),
    (INIT,'thankyou'):(INIT,1)
}

#Define respond()
def respond(state,message):
    (new_state,response) = policy_rules[(state,interpret(message))]
    return new_state,response

#Define interpret()
def interpret(message):
    data = interpreter.parse(message)
    state = data['intent']['name']
    return state


# In[13]:


import sys
import requests
import json

#Define get the weather of the whole country
def get_weather(msg,city):
    url = "http://v.juhe.cn/weather/index?format=2&cityname=%E8%8B%8F%E5%B7%9E&key"    
    key = '26f26b1e2eb850a9dba3710905dd9720'    
    data = {'key': key, "city": city}    
    req = requests.post(url, data)    
    info = dict(req.json())
    info = info['result']['future']
    print(info)
    
    number = msg
    newinfo = info[number]
    temperature = newinfo['temperature']
    weather = newinfo['weather']
    wind = newinfo['wind']
    week = newinfo['week']
    date = newinfo['date']
    response = 'Date: ' + date +"   " + week + '  temperature:  '+ temperature +'  weather:  ' + weather+ '  wind:  ' + wind
    return response


# In[14]:


from iexfinance.stocks import Stock
from datetime import datetime
from iexfinance.stocks import get_historical_data


#Define the price of the stock now
def get_now_price(msg):
    stock = Stock(msg)
    price = stock.get_price()
    return price

#Define get the price from the start of the end
def get_historical_price(msg,time):
    starttime = datetime(int(time[0]),int(time[1]),int(time[2]))
    endtime = datetime(int(time[3]),int(time[4]),int(time[5]))

    historical_pirce =  get_historical_data(msg,starttime,endtime)
    return historical_price


# In[15]:


import random

greet_responses = {
    'greet':['Hello,may I help you?',
             'What can I do for you?',
             "Nice to meet you, I'm ready to help you.",
            ],
    'thankyou':["You're welcom.",
               "It's my honor."
              ],
    'goodbye':["Goodbye",
              "Bye",
              "See you soon"
              ],
    'help':['Now I can only do                                    1. weather_forcast(seven days)                 2.stock_pirce_query']
}

#Define greet_respond()
def greet_respond(message):
    information = interpreter.parse(message)
    intent = information['intent']['name']
    
    if intent in greet_responses:
        key = intent
    return random.choice(greet_responses[key])


# In[16]:


import random
import re

ask_responses = {
    'weather_ask':['Which city do you want to know?',
                   'Could you please tell the exact city?'],
    'stock_ask':['Sorry,which stock?',
                 'Could you be more specific?'],
    'stock_historcial_ask':['Please tell me the time from start to the end.',
                          'Could you tell me the strat time and the end?'],
    'weekday_ask':['Could you tell me the exact date ?']
}

#Define ask_respond()
def ask_respond(message):
    information = interpreter.parse(message)
    intent = information['intent']['name']
    
    if intent in ask_responses:
        key = intent
    return random.choice(ask_responses[key])

#Define get_name()
def get_name(message):
    name = re.findall(r"[A-Z]+[a-z]*",message)
    return name

#Define state_change()
def state_change(state,message):
    print(interpret(message))
    new_state, response = policy_rules[(state, interpret(message))]
    print(response)
    
    if response == 1:
        return greet_respond(message)
    elif response == 2:
        return ask_respond(message)
    elif response == 3:
        return get_weather(0,message)
    elif response == 4:
        name = get_name(message)
        return get_now_price(name)
    elif repsonse == 5:
        stock = message
        return stock
    elif response == 6:
        weekday = get_time(message)
        return get_weather(weekday,city)
    elif response == 7:
        time = get_time(message)
        return get_historical_price(stock,time)

#Define reply()
def main(message):
    state = INIT
    response = state_change(state,message)
    print(response)

    return response


# In[17]:


#repsond the wechat friend
@bot.register(my_friend)
def reply_my_friend(msg):
    return main(msg.text)


# In[ ]:





# In[ ]:





# In[ ]:




