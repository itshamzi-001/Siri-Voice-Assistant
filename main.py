import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import naatLibrary
import requests
import threading
import random
import pyjokes
import datetime



recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "f7501d0bf2f542cfb56e72607ad9db0c"


def _speak_worker(text):
    engine = pyttsx3.init('sapi5')  
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def speak(text):
    t = threading.Thread(target=_speak_worker, args=(text,), daemon=True)
    t.start()


    
def processCommand(c):

    if "open google" in c.lower():
        speak("Opening Google.")
        webbrowser.open("https://google.com")

    elif "search" in c.lower():
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://google.com/search?q={query}")
        else:
            speak("What should I search for?")

    elif "open facebook" in c.lower():
        speak("Opening Facebook.")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn.")
        webbrowser.open("https://linkedin.com")

    elif "open chatgpt" in c.lower():
        speak("Opening ChatGPT.")
        webbrowser.open("https://chatgpt.com/")

    elif "joke" in c.lower():
        joke = pyjokes.get_joke()
        speak(joke)
        print(f"😂 {joke}")

    elif c.lower().startswith("play"):
        naats = c.lower().split(" ")[1]
        link = naatLibrary.naat[naats]
        speak(f"Playing {naats}.")
        webbrowser.open(link)

    elif "news" in c.lower():
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            if len(articles) > 0:
                random_headlines = random.sample(articles, min(1, len(articles)))

                speak("Here are some of the latest headlines.")
                print("📰 Top Headlines:\n")

                for i, article in enumerate(random_headlines, start=1):
                    print(f"{i}. {article['title']}")
                    speak(article['title'])
            else:
                speak("I couldn't find any news at the moment.")

    elif "time" in c.lower():
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
        print(f"🕒 {current_time}")

    elif "date" in c.lower():
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
        print(f"📅 {today}")

    elif any(word in c.lower() for word in ["exit", "quit", "stop"]):
        speak("Goodbye! Have a great day.")
        time.sleep(1)
    else:
        speak("I'm not sure how to do that yet.")
        print("Command recognized:", command)

if __name__ == "__main__":
    print("Initializing Siri...")
    speak("Initializing Siri")

    while True:
        try:
            with sr.Microphone() as source:
                print("\nListening for wake word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)

            try:
                word = recognizer.recognize_google(audio)
                if word.lower() == "hey siri":
                    print("Wake word detected ✅")
                    speak("yeah")
                    time.sleep(0.8)
                    with sr.Microphone() as source:
                        print("Siri Active... Listening for command...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source, timeout=6, phrase_time_limit=5)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)

            except sr.UnknownValueError:
                pass

        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print("Error:", e)



