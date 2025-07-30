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
    
    return query

def search_wikipedia(query = ''):
    try:
        searchResults = wikipedia.search(query)
        if not searchResults:
            return 'No result found on Wikipedia.'
        wikiPage = wikipedia.page(searchResults[0])
        return wikiPage.summary
    except wikipedia.DisambiguationError as e:
        wikiPage = wikipedia.page(e.options[0])
        return wikiPage.summary
    except Exception as e:
        return f"Error: {str(e)}"

def listOrDict (var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']
    
def search_wolframalpha(query = ''):
    try:
        response = wolframClient.query(query)
        if response['@success'] == 'false':
            return 'Could not compute.'
        
        pod1 = response['pod'][1]
        if (('result' in pod1['@title'].lower()) or
            (pod1.get('@primary', 'false') == 'true') or
            ('definition' in pod1['@title'].lower())):
            return listOrDict(pod1['subpod']).split('(')[0]
        else:
            return listOrDict(pod1['subpod']).split('(')[0]
    except Exception as e:
        return f"Error: {str(e)}"   
    


if __name__ == '__main__':
    speak('all systems are nominal. my name is hex and i am your ai assistant')

    while True:
        query = parseCommand()
        if not query:
            continue

        query = query.lower().split()

        if query[0] == activationWord:
            query.pop(0)

            # handle "say" command
            if query and query[0] == 'say':
                query.pop(0)
                speech = ' '.join(query)
                speak(speech)

            # handle "go to" (web navigation)
            elif len(query) > 2 and query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                search_term = ' '.join(query[2:])
                webbrowser.get('chrome').open_new_tab(f'https://{search_term}')

            # wikipedia search
            elif query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying Wikipedia...')
                result = search_wikipedia(query)
                speak(result)

            # wolfram Alpha
            elif query[0] in ['compute', 'calculate']:
                query = ' '.join(query[1:])
                speak('Computing...')
                result = search_wolframalpha(query)
                speak(result)

            # note-taking
            elif query[0] == 'log':
                speak('Ready to record.')
                new_note = parseCommand()
                if new_note:
                    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    filename = f'note_{now}.txt'
                    with open(filename, 'w') as file:
                        file.write(new_note)
                    speak('Note written.')

            # exit
            elif query[0] == 'exit':
                speak('goodbye.')
                break