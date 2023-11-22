import speech_recognition
import pyttsx3
import datetime
import command_handler as ch

def listen(check):
    # Initialize speech recognition and TTS engine
    recognizer = speech_recognition.Recognizer()

    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)

    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.50)

    WAKE_WORD = "hello computer"

    while True:
        if not check:
            break
        try:
            # Initialize microphone input
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                # Convert audio to text
                text = recognizer.recognize_whisper(audio, translate=True)
                text = text.lower()
                print(f'Log: {text}')

                # If WAKE_WORD is catched continue with command
                if WAKE_WORD in text:
                    # engine.say('Hello Nick.')
                    # engine.runAndWait()
                    hour = datetime.datetime.now().hour
                    if hour >= 0 and hour < 12:
                        engine.say("Good Morning")
                        engine.runAndWait()
                    elif hour >= 12 and hour < 18:
                        engine.say("Good Afternoon")
                        engine.runAndWait()
                    elif hour >= 18 and hour < 24:
                        engine.say("Good evening")
                        engine.runAndWait()
                    else:
                        engine.say("Good Night")
                        engine.runAndWait()
                    command = text.replace(WAKE_WORD, '').strip()
                    if command:
                        # Cleaning up command
                        if ',' in command:
                            command = command.strip(',')
                            command = command.lstrip()
                        print(f'Command: {command}')
                        ch.command_handler(command, engine)

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            continue