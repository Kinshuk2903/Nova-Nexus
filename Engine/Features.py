import os
from pipes import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
from Engine.Command import Speak
from Engine.Config import ASSISTANT_NAME
import pywhatkit as kit
from Engine.Helper import Remove_words, extract_yt_term
from hugchat import hugchat

# Playing assistant sound function

@eel.expose
def PlayAssistSound():
    music_dir = "C:\\Users\\KIIT\\Desktop\\Project NovaNexus\\Www\\Assests\\Audio\\start_sound.mp3"
    playsound(music_dir)

con = sqlite3.connect("NovaNexus.db")
cursor = con.cursor()

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                Speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    Speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    Speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        Speak("not found")
        except:
            Speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    Speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(access_key="XsDO7D32Gpc+NR2/PeZMt60FnVVJnvlFi0pCeeZ9NkTSaWsO9UGZtg==",keyword_paths=["Nexus/nexus_en_windows_v3_0_0.ppn"])

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for hotword...")
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)
            if keyword_index>=0:
                print("HotWord Detected")

                # pressing shorcut key win+n
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

if __name__ == "__main__":
    hotword()

# find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = Remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        Speak('not exist in contacts')
        return 0, 0
    
    
def whatsApp(mobile_no, message, flag, name):

    # Encode the message once
    encoded_message = quote(message)
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Open WhatsApp chat
    os.startfile(whatsapp_url)
    time.sleep(5)  # Wait for chat to load

    # Message sending
    if flag == 'message':
        pyautogui.press('enter')
        Speak(f"Message sent successfully to {name}")

    # Voice call
    elif flag == 'call':
        for _ in range(11):  
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        Speak(f"Calling {name}")

    # Video call
    elif flag == 'video call':
        for _ in range(10):  
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        Speak(f"Starting video call with {name}")

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="Engine/Cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    Speak(response)
    return response
