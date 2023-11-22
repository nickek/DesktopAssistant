import speech_recognition
import pyttsx3
import datetime
import re
import command_handler as ch
import logging
logging.basicConfig(filename='DesktopAssistant.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("comtypes.client._code_cache").setLevel(logging.ERROR) # Suppress INFO messages from comtypes.client._code_cache logger


def listen(check):
    try:
        # Initialize speech recognition and TTS engine
        recognizer = speech_recognition.Recognizer()
        recognizer.energy_threshold = 400
        recognizer.dynamic_energy_threshold = False
        
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
                    audio = recognizer.listen(mic, timeout=0.5)

                    # Convert audio to text
                    text = recognizer.recognize_whisper(audio, translate=True)
                    
                    if text:
                        # Cleaning up text
                        text = text.lower()
                        text = remove_special_characters(text)
                        logging.info(f'Message: {text}')

                    print(f'Log: {text}')

                    # If WAKE_WORD is catched continue with command
                    if WAKE_WORD in text:
                        # engine.say('Hello Nick.')
                        # engine.runAndWait()
                        hour = datetime.datetime.now().hour
                        if hour >= 0 and hour < 12:
                            logging.info(f'Response: Good Morning')
                            engine.say("Good Morning")
                            engine.runAndWait()
                        elif hour >= 12 and hour < 18:
                            logging.info(f'Response: Good Afternoon')
                            engine.say("Good Afternoon")
                            engine.runAndWait()
                        elif hour >= 18 and hour < 24:
                            logging.info(f'Response: Good Evening')
                            engine.say("Good Evening")
                            engine.runAndWait()
                        else:
                            logging.info(f'Response: Good Night')
                            engine.say("Good Night")
                            engine.runAndWait()
                        command = text.replace(WAKE_WORD, '').strip()
                        if command:
                            command = command.lstrip()
                            logging.info(f'Command: {command}')
                            print(f'Command: {command}')
                            ch.command_handler(command, engine)

            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                recognizer.energy_threshold = 400
                recognizer.dynamic_energy_threshold = False
                continue

    except Exception as e:
        print(f'Error: {e}')
        logging.error(e)

def remove_special_characters(input_string):
    try:
        # Define a regular expression pattern to match special characters
        pattern = r'[^a-zA-Z0-9\s]'  # This pattern allows alphanumeric characters and whitespace

        # Use re.sub() to replace matched characters with an empty string
        result_string = re.sub(pattern, '', input_string)

        return result_string
    except Exception as e:
        print(f'Error: {e}')
        logging.error(e)