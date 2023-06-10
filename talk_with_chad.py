import openai
import subprocess
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)


def get_password(service_name):
    """Get the password for the given service."""
    result = subprocess.run(
        ["security", "find-generic-password", "-s", str(service_name), "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


openai.api_key = get_password("openai-api-key")

# Initialize conversation history with a system message that sets
# the behavior of the assistant
conversation_history = [
    {
        "role": "system",
        "content": "As a diligent assistant, please ensure all answers are thoroughly researched, cross-checked with the most recent sources, and supplied in an accurate and well-informed manner."
    },
]


# Function to calculate total tokens in conversation
def calculate_token_count(conversation_messages):
    """Calculate the total number of tokens in a list of messages."""
    return sum([len(openai.Tokenizer().encode(message["content"])) for message in conversation_messages])


# Function to truncate conversation to fit within token limit
def truncate_conversation_to_fit_token_limit(conversation_messages, max_tokens=4096):
    """Truncate the conversation messages to ensure they fit within the maximum token limit."""
    total_tokens = calculate_token_count(conversation_messages)
    while total_tokens > max_tokens:
        # Remove oldest messages first
        conversation_messages.pop(0)
        total_tokens = calculate_token_count(conversation_messages)
    return conversation_messages


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

    # Send a chat message to the API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use an existing model
        messages=conversation_history
    )

    # Append assistant's response to conversation history
    assistant_message = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": assistant_message})

    # Print the assistant's response
    print(f"{Fore.LIGHTGREEN_EX}AI: {assistant_message}")
