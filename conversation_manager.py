import json
import os
import time

# Path to the JSON file where conversations will be stored
CONVERSATIONS_FILE = 'conversations.json'

# Load conversations from file at startup
def load_conversations():
    try:
        if os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, 'r') as f:
                return json.load(f)
    except json.JSONDecodeError:
        print("Failed to load conversations.json due to a JSONDecodeError. Starting fresh.")
    return {}

# Save conversations to file
def save_conversations(conversations):
    with open(CONVERSATIONS_FILE, 'w') as f:
        json.dump(conversations, f, indent=4)

# Function to update the conversation context
def update_conversation(conversations, guild_id, channel_id, user_input, bot_response):
    # Use a string key instead of a tuple
    key = f"{guild_id}-{channel_id}"
    if key in conversations:
        conversations[key]["context"] += f"\nUser: {user_input}\nBot: {bot_response}"
    else:
        conversations[key] = {"context": f"User: {user_input}\nBot: {bot_response}", "last_active": time.time()}
    
    conversations[key]["last_active"] = time.time()
    save_conversations(conversations)  # Save the updated conversation

# Function to get the conversation context
def get_conversation(conversations, guild_id, channel_id, context_timeout):
    # Use a string key instead of a tuple
    key = f"{guild_id}-{channel_id}"
    if key in conversations:
        if time.time() - conversations[key]["last_active"] < context_timeout:
            return conversations[key]["context"]
        else:
            conversations[key] = {"context": "", "last_active": 0}
    return None
