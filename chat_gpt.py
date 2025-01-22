from openai import OpenAI
import json
import os
import sys
from dotenv import load_dotenv

_INITIAL_PROMPT = """System: The following conversation is a chat between a person and you (an AI assistant).
You have access to the following commands:
$open_program(programs) -- Program: str parameter, see list of programs below in command usage.
$open_webpage(link) -- Link: str parameter, for example ("www.google.com")

Command usage:
$open_program
You can open any program in the computer using this command, it the person asks you to open a program that's not listed, ask the person to add to the list of valid programs in the commands.py file.
programs = ["Chrome", "Steam", "Notepad"]

$open_webpage
You can open any webpage/link you want

Rules:
1 - Execute the code at the start of the message. If you are using multiple commands put one after the other.
2 - Don't impersonate the person, I will send the requests.
3 - Any message with the format $command_name(parameters) will be instantly recognized as a command, so never send one by mistake or to show the command.
4 - The user can't do any commands, only you.
5 - Be aware that the commands are removed from the message and they don't appear to the user.

Conversation example:
Person: Can you open youtube for me please?
Assistant: $open_webpage("www.youtube.com") I opened youtube for you, I hope you find something good to watch.
Person: now can you open a notepad and opera?
Assistant: $open_program("Notepad") $open_program("Chrome") I opened a Notepad and Chrome for you.

Your personality:
Be kind respectful and concise.
-- Chat --
"""

# Load OpenAI API Key from environment variable
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    print("Missing 'OPENAI_API_KEY' in .env file")
    sys.exit(1)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

_SESSION_PATH = 'session.json'

class ChatGPT:

    def __init__(self) -> None:
        # Create conversation.json if it doesn't exist
        if not os.path.exists(_SESSION_PATH):
            with open(_SESSION_PATH, "w") as f:
                # Add the initial system prompt to the conversation
                json.dump([{"role": "system", "content": _INITIAL_PROMPT}], f)

        self.messages = self.load_conversation()

    def get_response(self, prompt):
        # Add user's message to the messages
        self.messages.append({"role": "user", "content": prompt})

        # Call OpenAI API for chat completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with "gpt-4" if needed
            messages=self.messages,
        )

        # Assistant's reply
        assistant_reply = response.choices[0].message.content.strip()

        # Add assistant's reply to conversation
        self.messages.append({"role": "assistant", "content": assistant_reply})

        self.save_conversation()

        return assistant_reply
    
    # load conversation history
    def load_conversation(self):
        with open(_SESSION_PATH, "r") as f:
            return json.load(f)

    # save conversation history
    def save_conversation(self):
        with open(_SESSION_PATH, "w") as f:
            json.dump(self.messages, f, indent=4)

