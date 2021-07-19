import webbrowser
import random


def calculator():
    return "<div>Ok Done<script>window.open('https://meutshuk.github.io/calculator/');</script></div>"


def calender():
    return "<div>Ok Done<script>window.open('https://www.rapidtables.com/tools/calendar.html');</script></div>"


def notepad():
    return "<div>Ok Done<script>window.open('https://www.rapidtables.com/tools/notepad.html');</script></div>"


def passwordGenerator():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@£$%^&*().,?0123456789'
    password = ''
    for c in range(10):
        password += random.choice(chars)
    return "Password generated is " + password


def direction(text):
    url = "https://www.google.com/maps?q=" + text
    return """
    <div>Ok Done<script>window.open('%s');</script></div>
    """ % url


def openMap():
    return "<div>Ok Done<script>window.open('https://www.google.com/maps/');</script></div>"


def searchYoutube(text):
    blankText = " "
    wordList = ['search', 'youtube']
    newWord = text.split()
    for word in list(newWord):
        if word.lower() in wordList:
            newWord.remove(word)
    url = "https://www.youtube.com/results?search_query=" + blankText.join(newWord)
    return """
        <div>Ok Done<script>window.open('%s');</script></div>
        """ % url


def coinToss():
    option = ['Heads', 'Tails']
    return random.choice(option)
