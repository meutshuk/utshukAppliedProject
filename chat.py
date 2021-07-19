#! /usr/bin/python3
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
import csv
import os
from botConfig import myBotName, chatBG, botAvatar, useGoogle, confidenceLevel
import playsound
from gtts import gTTS

# Experimental Date Time
from dateTime import getTime, getDate
from extraModule import calculator, calender, passwordGenerator, notepad, direction, openMap, searchYoutube, coinToss

import logging

logging.basicConfig(level=logging.INFO)

application = Flask(__name__)

chatbotName = myBotName
print("Bot Name set to: " + chatbotName)
print("Background is " + chatBG)
print("Avatar is " + botAvatar)
print("Confidence level set to " + str(confidenceLevel))

# Create Log file
try:
    file = open('BotLog.csv', 'r')
except IOError:
    file = open('BotLog.csv', 'w')

bot = ChatBot(
    "ChatBot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': confidenceLevel,
            'default_response': 'Sorry I dont know'
        }
    ],
    response_selection_method=get_random_response,
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="botData.sqlite3"
)

bot.read_only = True
print("Bot Learn Read Only:" + str(bot.read_only))


# path = os.getcwd()+""
# os.chdir(path)


def sound(text):
    tts = gTTS(text=text, lang='en')
    filename = 'sound.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def weather(text):
    url = "https://www.google.com/search?q=" + text
    html = requests.get(url).content

    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    loc = soup.find('span', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    # formatting data
    data = str.split('\n')
    time = data[0]
    sky = data[1]

    # printing all data
    speakWord = " In " + loc + " temperature is " + temp + " with " + sky + " sky"
    sound(speakWord)
    return speakWord


def tryGoogle(myQuery):
    linkk = "https://www.google.com/search?q=" + myQuery
    print(linkk)
    return "<br><br>Here is what I found on Google: <a target='_blank' href='" + linkk + "'>" + myQuery + "</a>"


@application.route("/")
def home():
    return render_template("index.html", botName=chatbotName, chatBG=chatBG, botAvatar=botAvatar)


@application.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    youtubeWordList = ['search', 'youtube']
    if all(x in userText.lower() for x in youtubeWordList):
        botReply = searchYoutube(userText)
        sound("youtube opened")
        return botReply

    for i in userText.split():
        if i == 'weather':
            botReply = weather(userText)
            return botReply

        if i == 'direction':
            botReply = direction(userText)

            return botReply

    botReply = str(bot.get_response(userText))

    if botReply == "Sorry I dont know":
        sound("Sorry I dont know. here is a google search")
        botReply = str(bot.get_response('IDKnull'))  # Send the i don't know code back to the DB
        if useGoogle == "yes":
            botReply = botReply + tryGoogle(userText)

    elif botReply == "getTIME":
        botReply = getTime()
        sound(botReply)
        print(getTime())
    elif botReply == "getDATE":
        botReply = getDate()
        sound(botReply)
        print(getDate())

    elif botReply == "Calender":
        botReply = calender()
        sound("Ok")
    elif botReply == "Calculator":
        botReply = calculator()
        sound("Ok")
    elif botReply == "Notepad":
        botReply = notepad()
        sound("Ok")
    elif botReply == 'password':
        botReply = passwordGenerator()
        sound("Password generated")
    elif botReply == 'map':
        botReply = openMap()
        sound("Ok")
    elif botReply == 'coinToss':
        botReply = coinToss()
        sound(botReply)
    else:
        sound(botReply)

    # Log to CSV file
    print("Logging to CSV file now")
    with open('BotLog.csv', 'a', newline='') as logFile:
        newFileWriter = csv.writer(logFile)
        newFileWriter.writerow([userText, botReply])
        logFile.close()
    return botReply


if __name__ == "__main__":
    # application.run()
    application.run(debug=True)
