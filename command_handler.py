import subprocess
import sys
import datetime
import webbrowser
import logging
logging.basicConfig(filename='DesktopAssistant.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("comtypes.client._code_cache").setLevel(logging.ERROR) # Suppress INFO messages from comtypes.client._code_cache logger


def command_handler(command, engine):

    if 'google' in command:
        search = command.replace('google', '').strip()
        webbrowser.open(f'https://www.google.com/search?q={search}')
        logging.info(f'Response: Opening a new google tab and searching {search}')
        engine.say(f'Opening a new google tab and searching {search}')
        engine.runAndWait()
        return
    
    elif 'shut down' in command:
        if 'cancel' in command:
            subprocess.run('shutdown /a', shell=True)
            logging.info('Response: Okay cancelled shutdown.')
            engine.say('Okay cancelled shutdown.')
            engine.runAndWait()
            return
        if 'hour' or 'minute' or 'second' in command:
            time = extract_time_from_string(command)
            print(time)
            subprocess.run(f'shutdown /s /t {time}', shell=True)
            time_string = seconds_to_human_readable(time)
            logging.info(f'Response: Okay, shutting down in {time_string}.')
            engine.say(f'Okay, shutting down in {time_string}.')
            engine.runAndWait()
        else:
            subprocess.run('shutdown /s /t 3600', shell=True)
            logging.info('Response: Okay shutting down in one hour.')
            engine.say('Okay shutting down in one hour.')
            engine.runAndWait()
            return

    elif 'date' in command:
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        year = datetime.datetime.now().year
        logging.info(f"Response: Todays date is {month} {day} {year}")
        engine.say(f"Todays date is {month} {day} {year}")
        engine.runAndWait()
        return

    elif 'time' in command:
        Time = datetime.datetime.now().strftime("%H:%M:%S")
        logging.info(f'Response: The current time is {Time}')
        engine.say(f'The current time is {Time}')
        engine.runAndWait()
        return

    elif 'exit' in command:
        logging.info('Response: Okay exitting program.')
        engine.say('Okay exitting program.')
        engine.runAndWait()
        sys.exit()

    else:
        logging.info(f'Response: I Cant find the command: {command}.')
        engine.say(f'I Cant find the command: {command}.')
        engine.runAndWait()
        return
    

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
    except (ValueError, IndexError):
        return "Invalid input. Please provide a valid time format."
    

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
    except ValueError:
        return "Invalid input. Please provide a valid number of seconds."