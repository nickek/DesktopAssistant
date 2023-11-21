import subprocess
import sys
import datetime


def command_handler(command, engine):
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    year = datetime.datetime.now().year

    if 'shut down' in command:
        if 'cancel' in command:
            subprocess.run('shutdown /a', shell=True)
            engine.say('Okay cancelled shutdown.')
            engine.runAndWait()
            return
        if 'hour' or 'minute' or 'second' in command:
            time = extract_time_from_string(command)
            print(time)
            subprocess.run(f'shutdown /s /t {time}', shell=True)
            time_string = seconds_to_human_readable(time)
            engine.say(f'Okay, shutting down in {time_string}.')
            engine.runAndWait()
        else:
            subprocess.run('shutdown /s /t 3600', shell=True)
            engine.say('Okay shutting down in one hour.')
            engine.runAndWait()
            return

    elif 'date' in command:
        engine.say("Todays date is: ")
        engine.say(month)
        engine.say(day)
        engine.say(year)
        engine.runAndWait()
        return

    elif 'time' in command:
        Time = datetime.datetime.now().strftime("%H:%M:%S")
        engine.say('The current time is')
        engine.say(Time)
        engine.runAndWait()
        return

    elif 'exit' in command:
        engine.say('Okay exitting program.')
        engine.runAndWait()
        sys.exit()

    else:
        engine.say(f'I Cant find the command: {command}.')
        engine.runAndWait()
        return
    

def extract_time_from_string(input_str):
    try:
        # Split the string by whitespace to extract individual words
        words = input_str.split()

        for i, word in enumerate(words):
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