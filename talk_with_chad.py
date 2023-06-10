import openai
import subprocess
from colorama import init, Fore
import time
import threading
import concurrent.futures

# Initialize colorama
init(autoreset=True)


def get_password(service_name):
    """Get the password for the given service."""
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", str(service_name), "-w"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error while getting password: {e}")
        return None


try:
    openai.api_key = get_password("openai-api-key")
except Exception as e:
    print(f"Error while setting API key: {e}")
    exit(1)

# Initialize conversation history with a system message that sets the behavior of the assistant
conversation_history = [
    # your system messages
]


# Define your other functions here...


# Define a loading animation
class LoadingAnimation(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False

    def start_animation(self):
        self.running = True
        print("Thinking", end='', flush=True)
        self.start()

    def run(self):
        while self.running:
            print(".", end='', flush=True)
            time.sleep(1)

    def stop_animation(self):
        self.running = False


# Function to send a chat message to the API
def send_message(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return response
    except Exception as e:
        print(f"Error while creating chat completion: {e}")
        return None


# Interact with the model
while True:
    # Prompt the user for input
    user_input = input(f"{Fore.LIGHTYELLOW_EX}You (type 'quit' to exit): ")
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
