import subprocess
import sys
import datetime
import webbrowser
import logging
import requests
import speech_recognition
import voice_handler
logging.basicConfig(filename='DesktopAssistant.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("comtypes.client._code_cache").setLevel(logging.ERROR) # Suppress INFO messages from comtypes.client._code_cache logger


def command_handler(command, engine):
    try:
        if 'google' in command:
            google(command, engine)
            return
        
        elif 'shut down' in command or 'shutdown' in command:
            shutdown(command, engine)
            return

        elif 'date' in command:
            date(command, engine)
            return

        elif 'time' in command:
            time(command, engine)
            return

        elif 'weather' in command:
            get_weather(command, engine)
            return

        elif 'exit' in command:
            program_exit(command, engine)

        else:
            cant_find(command, engine)
            return
        
    except Exception as e:
        print(f'Error: {e}')
        logging.error(e)
    

def google(command, engine):
    search = command.replace('google', '').strip()
    webbrowser.open(f'https://www.google.com/search?q={search}')
    logging.info(f'Response: Opening a new google tab and searching {search}')
    engine.say(f'Opening a new google tab and searching {search}')
    engine.runAndWait()
    return


def shutdown(command, engine):
    if 'cancel' in command:
        subprocess.run('shutdown /a', shell=True)
        logging.info('Response: Okay cancelled shutdown.')
        engine.say('Okay cancelled shutdown.')
        engine.runAndWait()
        return
    if 'hour' or 'minute' or 'second' in command:
        time = extract_time_from_string(command)
        subprocess.run(f'shutdown /s /t {time}', shell=True)
        time_string = seconds_to_human_readable(time)
        logging.info(f'Response: Okay, shutting down in {time_string}.')
        engine.say(f'Okay, shutting down in {time_string}.')
        engine.runAndWait()
        return
    else:
        subprocess.run('shutdown /s /t 3600', shell=True)
        logging.info('Response: Okay shutting down in one hour.')
        engine.say('Okay shutting down in one hour.')
        engine.runAndWait()
        return


def date(command, engine):
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    year = datetime.datetime.now().year
    logging.info(f"Response: Todays date is {month} {day} {year}")
    engine.say(f"Todays date is {month} {day} {year}")
    engine.runAndWait()
    return


def time(command, engine):
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    logging.info(f'Response: The current time is {Time}')
    engine.say(f'The current time is {Time}')
    engine.runAndWait()
    return


def program_exit(command, engine):
    logging.info('Response: Okay exitting program.')
    engine.say('Okay exitting program.')
    engine.runAndWait()
    sys.exit()


def cant_find(command, engine):
    print(command)
    logging.info(f'Response: I Cant find the command: {command}.')
    engine.say(f'I Cant find the command: {command}.')
    engine.runAndWait()
    return


def get_weather(command, engine):
    key = 'd94f6a181d6172e5246b69c78f20892d'
    engine.say('What city would you like to know the weather for?')
    engine.runAndWait()
    city = get_city()
    engine.say("Getting weather for " + city)
    engine.runAndWait()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=imperial'.format(city, key)

    resi = requests.get(url)
    data = resi.json()
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    cloudiness = data['clouds']['all']
    visibility = data['visibility']

    engine.say("Weather outside is {}".format(description))
    engine.say(
        "Temperatures today are {} degrees Fahrenheit but it feels like {} degrees Fahrenheit".format(temp, feels_like))
    engine.say("Humidity percentage is {} today".format(humidity))
    engine.say("Winds speeds are currently {}".format(wind_speed))
    engine.say("Cloud coverage is at {} percent today".format(cloudiness))
    engine.say("Visibility is {} percent today".format(visibility))
    engine.runAndWait()
    return


def get_city():
    try:
        recognizer = speech_recognition.Recognizer()
        # Initialize microphone input
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            # Convert audio to text
            city = recognizer.recognize_whisper(audio, translate=True)

            if city:
                # Cleaning up text
                city = city.lower()
                city = voice_handler.remove_special_characters(city)
                logging.info(f'Message: {city}')

            print(f'Log: {city}')

    except Exception as e:
        print(f'Error: {e}')
        logging.error(e)
    return city


def extract_time_from_string(input_str):
    try:
        # Split the string by whitespace to extract individual words
        words = input_str.split()
        t = {'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}

        for i, word in enumerate(words):
            if word.lower() in t:
                # Replace the word with its numeric value
                words[i] = str(t[word.lower()])
            if 'hour' in word:
                # Convert hours to seconds
                seconds = int(words[i - 1]) * 3600
                return seconds
            elif 'minute' in word:
                # Convert minutes to seconds
                seconds = int(words[i - 1]) * 60
                return seconds
            elif 'second' in word:
                # Extract seconds
                seconds = int(words[i - 1])
                return seconds

        # If no unit is specified, assume seconds
        return int(words[0])
    
    except ValueError as e:
        print(f'Error: {e}')
        logging.error(e)
        raise "Invalid value"
    
    except IndexError as e:
        print(f'Error: {e}')
        logging.error(e)
        raise "Invalid index"


def seconds_to_human_readable(seconds):
    try:
        # Convert seconds to hours, minutes, and remaining seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Build the time string
        time_string = ""
        if hours > 0:
            time_string += f"{hours} {'hour' if hours == 1 else 'hours'}"
        if minutes > 0:
            time_string += f" {minutes} {'minute' if minutes == 1 else 'minutes'}"
        if seconds > 0:
            time_string += f" {seconds} {'second' if seconds == 1 else 'seconds'}"

        return time_string.strip()
    
    except ValueError as e:
        print(f'Error: {e}')
        logging.error(e)
        raise "Invalid value"