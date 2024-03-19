import speech_recognition as sr
from random import choice
from gtts import gTTS
import pyttsx3
import json
import time
from AppOpener import open as run
from AppOpener import close
import requests
from bs4 import BeautifulSoup

with open('cases.json') as user_file:
    CASES = json.load(user_file)

STARTS = ["hey bot","hello bot","hello","hey","hey you"]
STOPS = ["stop bot","exit","end bot","stop","end"]
WRITE = ["notes","want take a note","text"]

guy = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
girl = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

def check(string_list,input_string):
    for s in string_list:
        if s.lower() in input_string.lower():
            return True
    return False

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def handling_listening():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)    
        main_playing(text)

    except sr.UnknownValueError:
        play("Sorry, I could not understand the audio.")
    except sr.RequestError:
        play("Sorry, there was an error connecting to the Google API. Please check your internet connection.")


def analyzer(text):
    text2 = text.split()
    if text2[0].lower() == "open":
        return "run"
    elif text2[0].lower() == "close":
        return "close"
    elif text2[0].lower() == "write":
        return "write"
    elif text2[0].lower() == "gold":
        return "gold"
    else:
        return False


def handle_analyzer(text):
    text2 = text.split()
    if analyzer(text) == "run":
        play(f"Opening {text2[1]}")
        run(text2[1])
    elif analyzer(text) == "close":
        play(f"Closing {text2[1]}")
        close(text2[1])
    elif analyzer(text) == "write":
        file = create_file()
        writing(" ".join(text2[1:]),file)
        close_file(file)
        play("File Created")
    elif analyzer(text) == "gold":
        play(f"Gold Price Is: {gold_price()}")


def listening():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        if check(STARTS,text):
            play("Hey .. How I Can Help You?")
            handling_listening()
            listening()
        elif check(STOPS,text):
            play("App Exiting..")
            exit()
        elif check(WRITE,text):
            play("Starting Write Mode..")
            write_mode()
            listening()
        elif analyzer(text):
            handle_analyzer(text)
            listening()
        else:
            listening()
    except sr.UnknownValueError:
        listening()
    except sr.RequestError:
        listening()



def check_case(case,text):
    if check(CASES[case][0],text):
        return True
    else:
        return False

def check_main(text,cases=CASES):
    for case in cases:
        if check_case(case,text):
            return case
    return False

def choicing(case,cases=CASES):
    return choice(cases[case][1])



def handling(text,case,reply):
    if check(case,text):
        return choice(reply)
    else:
        return False

def main_handling(text,cases=CASES):
    if check_main(text,cases):
        return choicing(check_main(text,cases))
    else:
        return False

def printing(text,case,reply):
    if handling(text,case,reply):
        print(handling(text,case,reply))


def main_printing(text,cases=CASES):
    if main_handling(text,cases):
        print(main_handling(text,cases))
    else:
        print("I Don't Know How To Answer Your Talking")

def play(text,voice=guy,volume=1.0,speed=150):
    engine = pyttsx3.init()
    engine.setProperty('voice', voice) # change voice to guy or girl
    engine.setProperty("rate", {volume})  # Speed of speech (words per minute)
    engine.setProperty("volume", {speed})  # Volume (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()


def handling_audio(text,case,reply):
    if check(case,text):
        return choice(reply)
    else:
        return False

def playing(text,case,reply):
    if handling_audio(text,case,reply):
        play(handling_audio(text,case,reply))

def main_playing(text,voice=guy,cases=CASES):
    if main_handling(text,cases):
        play(main_handling(text,cases),voice)
    else:
        play("I Don't Know How To Answer Your Talking")



###############################################################

def random_name():
    return str(round(time.time()*1000))[6:]



def create_file():
    f = open(f"{random_name()}.txt", "a")
    return f

def writing(text,file):
    file.write(text+"\n")

def close_file(file):
    file.close()


def write_mode():
    file = create_file()
    play("file created..")
    time.sleep(0.5)
    play("now say what you want to write..")
    while True:    
        text = listen()
        if text == "stop":
            play("ok stop the writing mode.")
            break
        elif text == "":
            pass
        else:
            writing(text,file)
    close_file(file)


########################################

def gold_price():
    url = "https://wikigerman.net/gold-jo/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text,"html.parser")
    price = soup.find_all("table", {"class": "gold-table"})[1].contents[1].contents[0].contents[2].contents[0]
    return price


########################################

