# welcome to the main file of the hedge project 
# starting with the necessary imports for the assistant 
# file name main.py - last edit 23/7/2025

import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import requests
import wolframalpha
import flask
import pyaudio

# speech engine intialisation 
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # 0 = male, 1 = female
activationWord = 'computer' #activiation word for the computer to start listening

# configure a browser for the ai to use
# setting the path 
chrome_path = r"C: \Program Files\Google\Chrome\Application\chrome.exe" # need to redo
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser (chrome_path))

#wolfram alpha client for math queries
appId = '5R49J7-J888YX9J2V'
wolframClient = wolframalpha.Client(appId)

# defining global variables
def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print('ready for command') #prints when computer is listening for a command

    with sr.Microphone() as source:
        listener.pause_thresehold = 2 
        input_speech = listener.listen(source)
    try:
        print ('processing speech...')
        query = listener.recognize_google(input_speech, language = 'en_gb')
        print(f'the inputed speech was {query}')
    except Exception as exception:
        print('i didnt catch that')
        speak('i didnt catch that')
        print(exception)
    return 'None'
    return query #unused command?

def serach_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('no wikipedia results sorry :(')
        return 'no result recieved'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DismabiguationEror as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict (var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']
    
def search_wolframalpha(query = ''):
    response = wolframClient.query(query)

    if response['@sucess'] == 'false':
        return 'could not compute'
    
    else:
        result = ''
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
    
    if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):

        result = listOrDict(pod1['supod'])

        return result.split('(')[0]
    
    else:
        question = listOrDict(pod1['subpod'])

        return question.split('(')[0]
    
        speak('computation failed. querying universal databank')
        return search_wikipedia(question)    
    


if __name__ == '__main__':
    speak('all sys nominal.')

    while True: 

        query = parseCommand().lower().split()

    if query[0] == activationWord:
        query.pop(0)

    if query[0] == 'say':
        if 'hello' in query:
            speak('greetings')
        else:
            query.pop(0) # remove say 
            speech = ''.join(query)
            speak(speech)
        
        # navigation 
        if query[0] == 'go' and query [1] == 'to':
            speak('opening...')
            query = ' '.join(query[2:])
            webbrowser-get('chrome').open_new(query)
        
        # wikipedia
        if query[0] == 'wikipedia':
            query = ' '.join(query[1:])
            speak('querying the universal databank')
            speak(search_wikipedia(query))

        # wolfram alpha 
        if query[0] == 'commpute' or query[0] == 'computer':
            query = ''.join(query[1:])
            speak('commputing')
        try:
            result = search_wolframalpha(query)
            speak(result)
        except:
            speack('unable to connect')

        #notetaking 

        if query[0] == 'log':
            speak('ready to record')
            newnote = parseCommand().lower()
            now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            with open('note_%d.txt' % now, 'w') as NewFile:
                newFile.write(newNote)
            speak('note written')

        if query[0] == 'exit':
            speak('bye')
            exit()


