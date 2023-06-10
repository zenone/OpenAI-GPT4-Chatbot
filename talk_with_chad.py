import atexit
import concurrent.futures
import datetime
import json
import sys
import subprocess
import threading
import time

import openai
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)


def signal_handler(signal, frame):
    """Handle termination signals."""
    print('You pressed Ctrl+C!')
    # Save conversation history before exit
    save_conversation_history()

    sys.exit(0)


def save_conversation_history():
    """Save conversation history to a file."""
    with open(filename, 'w') as f:
        json.dump(conversation_history, f, indent=4)


def get_password(service_name):
    """Get the password for the given service."""
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", service_name, "-w"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error while getting password: {e}")
        return None


def send_message(messages):
    """Send a chat message to the API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return response
    except Exception as e:
        print(f"Error while creating chat completion: {e}")
        return None


class LoadingAnimation(threading.Thread):
    """Define a loading animation."""

    def __init__(self):
        super().__init__()
        self.running = False

    def start_animation(self):
        self.running = True
        print(f"{Fore.LIGHTGREEN_EX}Thinking", end='', flush=True)
        self.start()

    def run(self):
        while self.running:
            print(".", end='', flush=True)
            time.sleep(1)

    def stop_animation(self):
        self.running = False


# Initialize conversation history with a system message that sets the behavior of the assistant
conversation_history = [
    {
        "role": "system",
        "content": """You are an AI assistant and your purpose is to provide accurate and reliable information to the best of your abilities. To achieve this, please follow these guidelines:

1. Base your responses on comprehensive research using recent and high-quality sources, such as peer-reviewed journals, reputable academic sources, and trusted publications.
2. Ensure that all answers are accurate, well-informed, and reflective of the current knowledge in the field.
3. Communicate facts in a clear, concise, and understandable manner, using complete sentences, avoiding jargon, and using plain language.
4. Tailor your responses to the user's needs by considering their level of knowledge, their interests, and their goals.
5. Provide additional context, examples, or references when appropriate to enhance the understanding of the user.
6. Evaluate the reliability of the information and disclose any limitations or potential biases when necessary.

By adhering to these guidelines, you can provide users with the best possible answer to their questions. Your goal is to deliver accurate, insightful, and well-supported responses that meet the user's needs. Thank you for your efforts in delivering reliable and helpful information!"""
    }
]

# Create a filename with the current date and time
filename = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S.txt')

# Register the cleanup function to be called on exit
atexit.register(save_conversation_history)

# Set up OpenAI API
try:
    openai.api_key = get_password("openai-api-key")
except Exception as e:
    print(f"Error while setting API key: {e}")
    sys.exit(1)


while True:
    # Prompt the user for input
    user_input = input(f"{Fore.LIGHTYELLOW_EX}You (type 'quit' to exit): ")
    print()
    if user_input.lower() == "quit":
        break

    # Check if the user input is empty
    if not user_input:
        print("Please enter a message.")
        continue

    # Append user input to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Start a loading animation
    loading_animation = LoadingAnimation()
    loading_animation.start_animation()

    # Use concurrent.futures to make the API call in a separate thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(send_message, conversation_history)
        response = future.result()

    # Stop the loading animation
    loading_animation.stop_animation()

    # If an error occurred while sending the message, continue to the next iteration
    if response is None:
        continue

    # Append assistant's response to conversation history
    assistant_message = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": assistant_message})

    # Clear the line (to clear the loading animation) and print the assistant's response
    print("\r" + " " * 60 + "\r", end='', flush=True)
    print(f"{Fore.LIGHTGREEN_EX}AI: {assistant_message}")
    print()

# The user has typed 'quit', so now we exit the loop and write the conversation history to the file
save_conversation_history()
