from colorama import Fore, Back, Style
from settings import *
from run_commands import RunCommands
import colorama
import whisper
import time
import os
import subprocess
import threading
from microphone import Microphone
import pyttsx3
from chat_gpt import ChatGPT
import warnings

# Disable FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# Text to speech
engine = pyttsx3.init()

# Set the language
engine.setProperty('voice', engine.getProperty('voices')[1].id)

# Initialize commands
run_commands = RunCommands()

# Initialize colorama
colorama.init()

# Get chat gpt response
def get_gpt_response(prompt):
    msg = prompt
    return msg


# Typewriter effect
def typewrite(msg):
    print('Assistant: ', end='')

    for i in range(len(msg)):
        print(msg[i], end="", flush=True)
        time.sleep(0.02)

    print('\n', end='')


# Parse message, returns the final message and command
# Returns the plain text message (with no commands), and return the command (the first it gets)
def parse_message(msg):
    # Get first line of the message
    first_line = msg.splitlines()[0]

    # Get all command occurences in the first line
    commands = [x.group() for x in cmd_regex.finditer(first_line)]

    # Remove commands from the message
    msg = cmd_cleaner.sub('', msg)

    return msg, commands


def check_ffmpeg():
    try:
        # Try running the ffmpeg command to check if it's installed
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        return False
    

# Text to speech
def speak(msg):
    engine.stop()
    engine.say(msg)
    engine.startLoop()


model = None


def load_whisper_model():
    global model
    model = whisper.load_model("base")


microphone = Microphone()


# Voice recognition
voice_result = None


def listen(stop):
    global voice_result
    global model
    voice_result = None

    result = ''

    # Whether the person quit on purpose or not
    quit = False

    print(Fore.WHITE + Style.DIM + '[ENTER to leave] ' +
          Style.RESET_ALL + Fore.YELLOW + 'Listening: ', end='')

    microphone.start_capturing()

    while microphone.is_capturing():
        # Record audio
        microphone.capture()

        # If something set the stop variable to true, stops the thread
        if stop():
            quit = True
            break

    microphone.stop_capturing()
    time.sleep(0.1)

    result = model.transcribe("output.wav")['text'].strip()
    if result:
        print(end='\n')
        voice_result = result

    try:
        os.remove("output.wav")
    except Exception:
        pass

    return result


quit = False  # Quit the program
debug_mode = False  # Test commands


# Handles user input, including the speech-to-text
def get_user_input():
    global quit, debug_mode, voice_result

    # Listening thread
    x = None

    user_input: str = ''

    # Get user input (shouldn't be an empty string)
    while not user_input:
        user_input: str = input(Style.BRIGHT + 'You: ')

        # Remove unecessary blank spaces
        if user_input:
            user_input = " ".join(user_input.split())

        if user_input.startswith('$'):
            # Do user commands and set user_input var to empty (necessary to not leave this block)
            if user_input == '$voice':
                user_input = ''
                if check_ffmpeg():
                    # Yes this is kind of a hack. It basically clears the previous line.
                    # It's used to replace the "Listening: " string with the "You: " string
                    print('\033[A                             \033[A')

                    # Speech-to-text
                    # Execute in another thread
                    stop_thread = False  # Stops the thread when set to true
                    x = threading.Thread(
                        target=listen, args=(lambda: stop_thread,))
                    x.start()

                    # Press enter to continue the program
                    enter = input()

                    # Kill the thread
                    if x.is_alive():
                        stop_thread = True
                        x.join()

                    # Clear garbage and creates new line
                    # and clear it
                    print(end='\n')
                    print('\033[A                             \033[A')

                    # Delete previous listening line, and inserts 'You: text'
                    print('\033[A                             \033[A')

                    # Warning message
                    if enter:
                        print(Style.RESET_ALL + Fore.RESET +
                            'System: Don\'t input characters when being asked to press enter.')

                    if voice_result:
                        user_input = voice_result
                        print(Style.RESET_ALL + Fore.RESET + 'You: ' + user_input)
                    else:
                        print(Style.RESET_ALL + Fore.RESET + 'You: ')
                else:
                    print(Style.RESET_ALL + Fore.RESET +
                          'System: FFmpeg is required for this feature. Please install it and try again.\n')

            # Quit loop
            elif user_input == '$quit':
                quit = True

            # Debug commands
            elif user_input == '$debug':
                debug_mode = not debug_mode

                if debug_mode:
                    print(Style.RESET_ALL + Fore.RESET +
                          'System: Debug mode activated, use $command_name(parameters) to test the command.')
                else:
                    print(Style.RESET_ALL + Fore.RESET +
                          'System: Debug mode deactivated.')
                    user_input = ''
                    continue
            else:
                if not debug_mode:
                    user_input = ''

        if not user_input:
            # No valid input
            print('\033[A                             \033[A')

    return user_input


def cleanup():
    global engine, microphone
    if microphone:
        microphone.close()
    engine.stop()


def main():
    print("Loading whisper...")
    load_whisper_model()

    try:
        # Get terminal size
        width = os.get_terminal_size().lines
        height = os.get_terminal_size().columns

        # Instancing chatgpt
        chat_gpt = ChatGPT()

        print(Style.DIM +
                '===============================================================')
        print('                  Welcome to AI Assistant                      ')
        print('                     Use $voice to talk                        ')
        print('                     Use $quit  to quit                        ')
        print('===============================================================' + Style.RESET_ALL)

        # Speaking thread
        speak_thread = None

        # Program loop
        while True:
            # Get a valid user input
            user_input: str = get_user_input()

            # Kill text-to-speech thread
            if speak_thread and speak_thread.is_alive():
                engine.endLoop()  # Stop speaking loop
                speak_thread.join()  # Kill thread

            # Quit program
            if quit:
                break

            # Debug mode to test commands
            if debug_mode:
                _, commands = parse_message(user_input)

                if commands:
                    for command in commands:
                        success = run_commands.run(command)
                continue

            # Get plain response and command (if there is any in the response)
            text, commands = parse_message(chat_gpt.get_response(user_input))

            # Say the text (text2speech)
            speak_thread = threading.Thread(target=speak, args=(text,))
            speak_thread.start()

            if commands:
                # Execute all found commands
                for command in commands:
                    # Run command
                    success = run_commands.run(command)

            # Outputs response
            print(Fore.CYAN, end='')
            typewrite(text)
            print(Fore.RESET, end='')
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()


if __name__ == '__main__':
    main()
