# ChatGPT-like Chat Bot

This is an interactive command-line chat bot that uses the OpenAI API to provide ChatGPT-like functionality with conversation history.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

You can get your API key from the [OpenAI Platform](https://platform.openai.com/api-keys).

3. Create an `input_meta.json` file to configure the chat bot:
```json
{
    "history_file": "chat_history.jsonl",
    "system_prompt_file": "system_prompt.txt",
    "model": "gpt-4o",
    "temperature": 0.7
}
```

## Usage

### Command Line
Run the chat bot directly:
```bash
python chat_bot.py
```

Or specify a custom configuration file:
```bash
python chat_bot.py my_config.json
```

### Desktop Shortcut (Windows)
For quick access, you can create a desktop shortcut:

1. Run the shortcut creation script:
```bash
powershell -ExecutionPolicy Bypass -File create_shortcut.ps1
```

2. A "ChatBot" shortcut will appear on your desktop
3. Double-click the shortcut to launch the chat bot in a new terminal window

The desktop shortcut uses the `launch_chatbot.bat` file which:
- Opens a new terminal window
- Navigates to the project directory
- Runs the chat bot
- Keeps the terminal open after exit

## Features

- Interactive conversation with context memory
- Conversation history saved to file
- Custom system prompts
- Configurable AI model and parameters
- Commands:
  - `exit`: Quit the chat bot
  - `DELETE HISTORY`: Clear conversation history

## Customization

You can modify the configuration in `input_meta.json`:
- `history_file`: File to store conversation history
- `system_prompt_file`: File containing the system prompt
- `model`: The OpenAI model to use (e.g., "gpt-4o", "gpt-4-turbo")
- `temperature`: Controls randomness (0.0 to 1.0) 