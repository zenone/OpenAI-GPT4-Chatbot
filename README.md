# 🤖 OpenAI Chatbot, aka Chad

Hello there! 👋 This is the repository for an interactive chatbot powered by OpenAI's GPT-4 model. This updated Python script interfaces with the OpenAI API to generate AI-powered responses and has enhanced error handling and multi-threading capabilities. 🧠

Whether you're testing, learning, or just having a bit of fun, this script provides a great starting point! 🚀 It's primarily an experimental script that I used to begin my journey in learning how to interact with GPT-4.

## 🚀 Getting Started

This chatbot uses your OpenAI API key, which should be kept securely. 🛡️ As I'm using a Mac, I've chosen to use the macOS Keychain to securely store the API key. Here's how I did it:

1. First, open your Terminal. 🖥️
2. Then, enter this command: `security add-generic-password -a $USER -s openai-api-key -w <openai_api_key>`

Make sure to replace `<openai_api_key>` with your actual OpenAI API key. This command securely stores your OpenAI API key in the macOS Keychain.

## 🌈 Colorful Interactions

To make the chat interaction more lively and distinguishable, the script uses the [Colorama](https://pypi.org/project/colorama/) library. This library allows us to print colored terminal text from Python, which is utilized to differentiate between user input and AI output. The user's prompt is in yellow, while the AI's response is in green.

## 📚 Code Overview

The Python script works as follows:

- First, it retrieves the OpenAI API key from the macOS Keychain using the `get_password` function. 🔑
- It then initializes a conversation history with a system message that instructs the GPT-4 model to act as a diligent assistant. 📝
- During the conversation with the model, it calculates the total number of tokens in the conversation to ensure it fits within the model's maximum token limit (4096 tokens for GPT-4). If the conversation exceeds the maximum token limit, it trims the oldest messages from the conversation history. 🧮
- It prompts the user for input (in yellow) and appends the input to the conversation history. 💬
- A loading animation is displayed while the message is being processed. The processing is done in a separate thread, allowing the animation to display without being blocked. 🔄
- It sends the conversation history to the OpenAI API and receives a response from the GPT-4 model. If an error occurs while sending the message, the error is handled gracefully, and the chat continues.
- Finally, it prints the model's response (in green) and adds it to the conversation history. 🖨️

It continues this process until the user types 'quit' to exit.

## 👩‍💻 Try It Out!

Feel free to clone this repository, replace `<openai-api-key>` with your actual OpenAI API key, and run the Python script to start chatting with the AI! Remember to keep your API keys safe and secure. Enjoy your colorful conversation with the AI! 💬🎉
