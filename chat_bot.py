#!/usr/bin/env python3

import os
import sys
import json
import argparse
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def load_prompt(prompt_file):
    """Load system prompt from file"""
    if os.path.exists(prompt_file):
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error loading prompt from {prompt_file}: {str(e)}")
            return None
    else:
        return None


def load_conversation_history(history_file):
    """Load conversation history from specified file if it exists"""
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        history.append(json.loads(line))
        except Exception as e:
            print(f"Error loading history from {history_file}: {str(e)}")
    return history


def save_to_history(role, content, history_file):
    """Save a message to specified history file"""
    timestamp = datetime.now().isoformat()
    message = {
        "role": role,
        "content": content,
        "timestamp": timestamp
    }
    try:
        with open(history_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(message) + '\n')
    except Exception as e:
        print(f"Error saving to history: {str(e)}")


def clear_history_file(history_file):
    """Clear the history file"""
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            f.write('')
        return True
    except Exception as e:
        print(f"Error clearing history file: {str(e)}")
        return False


def get_chat_response(prompt, client, system_prompt, history, model="gpt-4o", temperature=0.7, max_tokens=10000):
    """Get response from OpenAI API with context"""
    messages = []
    
    # Add system prompt if available
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add conversation history
    for entry in history:
        messages.append({"role": entry["role"], "content": entry["content"]})
    
    # Add current prompt
    messages.append({"role": "user", "content": prompt})
    
    try:
        # Make the API call
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"API error: {str(e)}")
        return None


def load_input_meta(meta_file):
    """Load configuration from input meta file"""
    try:
        with open(meta_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return (
                config.get('history_file'),
                config.get('system_prompt_file'),
                config.get('model', 'gpt-4o'),
                config.get('temperature', 0.7)
            )
    except Exception as e:
        print(f"Error loading input meta from {meta_file}: {str(e)}")
        sys.exit(1)


def main():
    """Main chat bot function"""
    parser = argparse.ArgumentParser(description='Interactive ChatGPT-like chat bot')
    parser.add_argument('input_meta', nargs='?', default='input_meta.json', 
                       help='Path to input meta JSON file containing history_file and system_prompt_file (default: input_meta.json)')
    
    args = parser.parse_args()
    
    # Load configuration from input meta
    history_file, system_prompt_file, model, temperature = load_input_meta(args.input_meta)
    
    if not history_file or not system_prompt_file:
        print("Error: input_meta file must contain 'history_file' and 'system_prompt_file' keys")
        sys.exit(1)
    
    # Validate OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not found.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        sys.exit(1)
    
    # Initialize OpenAI client
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Error initializing OpenAI client: {str(e)}")
        sys.exit(1)
    
    # Load system prompt
    system_prompt = load_prompt(system_prompt_file)
    if system_prompt is None:
        print(f"Warning: Could not load system prompt from {system_prompt_file}")
        print("Continuing without system prompt...")
    
    # Load conversation history
    history = load_conversation_history(history_file)
    print(f"Loaded {len(history)} previous messages from {history_file}")
    
    print("ChatBot initialized! Type 'exit' to quit.")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit condition
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            
            # Check for delete history command
            if user_input.upper() == 'DELETE HISTORY':
                print("Are you sure you want to clear history for this session? (yes/no): ", end="", flush=True)
                confirmation = input().strip().lower()
                if confirmation in ['yes', 'y']:
                    if clear_history_file(history_file):
                        history.clear()  # Clear in-memory history too
                        print("History cleared successfully!")
                    else:
                        print("Failed to clear history.")
                else:
                    print("History deletion cancelled.")
                continue
            
            if not user_input:
                print("Please enter a prompt or 'exit' to quit.")
                continue
            
            # Get response from API
            print("Assistant: ", end="", flush=True)
            response = get_chat_response(user_input, client, system_prompt, history, model, temperature)
            
            if response:
                print(response)
                
                # Save both prompt and response to history
                save_to_history("user", user_input, history_file)
                save_to_history("assistant", response, history_file)
                
                # Update in-memory history for context
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": response})
            else:
                print("Sorry, I couldn't generate a response. Please try again.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()