import openai
import pyttsx3
import speech_recognition as sr
import webbrowser
from apikey import api_data  

openai.api_key = api_data

Model = 'gpt-4o'  

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening.......')
        r.pause_threshold = 1 
        audio = r.listen(source)
    try:
        print('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that. Please try again.")
        return "None"
    return query

def Reply(question):
    try:
        completion = openai.ChatCompletion.create(
            model=Model,
            messages=[
                {'role': "system", 'content': "You are a helpful assistant."},
                {'role': 'user', 'content': question}
            ],
            max_tokens=200
        )
        answer = completion.choices[0].message['content']
        return answer
    except openai.OpenAIError as e:
        print(f"Error: {e}")
        return "Sorry, I am unable to get an answer right now."

if __name__ == '__main__':
    speak("Hello! How are you?")
    while True:
        query = takeCommand().lower()

        if query == "none":
            continue

        ans = Reply(query)
        print(ans)
        speak(ans)

        if "open youtube" in query:
            webbrowser.open('https://www.youtube.com')
        elif "open google" in query:
            webbrowser.open('https://www.google.com')
        elif "bye" in query:
            speak("Goodbye!")
            break