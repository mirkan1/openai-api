import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160) # sets the speaking speed of the engine
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id) # sets the voice of Microsoft David Desktop - English (United States)
    engine.say(text)
    engine.runAndWait()
    if engine._inLoop:
        engine.endLoop()
