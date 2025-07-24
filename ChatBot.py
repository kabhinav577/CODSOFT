import re  # Import regular expressions for pattern matching
import random  # Import random to choose random responses

# Dictionary to store context (like user's name)
context = {
    "name": None  
}

# Intent dictionary with regex patterns and predefined responses
intents = {
    "greeting": {
        "patterns": [r"\bhi\b", r"\bhello\b", r"\bhey\b"],
        "responses": ["Hello!", "Hi there!", "Hey! How can I help you?"]
    },
    "goodbye": {
        "patterns": [r"\bbye\b", r"\bgoodbye\b", r"\bfarewell\b"],
        "responses": ["Goodbye!", "See you soon!", "Take care!"]
    },
    "thanks": {
        "patterns": [r"\bthank\b", r"\bthanks\b", r"\bappreciate\b"],
        "responses": ["You're welcome!", "No problem!", "Happy to help!"]
    },
    "help": {
        "patterns": [r"\bhelp\b"],
        "responses": ["You can tell me your name, ask me how I'm doing, or just chat!"]
    }
}

# Dictionary to handle direct questions
direct_questions = {
    "how are you?": ["I'm doing great, thank you!", "I'm just a bot, but feeling helpful!"],
    "what is your name?": ["I’m ChatBot-101, your assistant.", "You can call me ChatBot!"],
    "what can you do?": ["I can remember your name, chat with you, and answer basic questions!"]
}

# Return a random response for a matched intent
def respond_to_intent(intent):
    return random.choice(intents[intent]["responses"])

# Match user input to intent using regex pattern search
def get_intent(user_input):
    for intent, data in intents.items():  
        for pattern in data["patterns"]:  
            if re.search(pattern, user_input):  
                return intent  
    return None  

# Handle memory-based responses (like remembering the user's name)
def handle_context(user_input):
    # Check if user is telling their name
    name_match = re.search(r"my name is (\w+)", user_input)
    if name_match:
        context["name"] = name_match.group(1).capitalize()  
        return f"Nice to meet you, {context['name']}!"

    # If user asks "what is my name", reply from memory
    if "what's my name" in user_input or "what is my name" in user_input:
        if context["name"]: 
            return f"Your name is {context['name']}!"
        else: 
            return "I don't know your name yet. You can tell me by saying 'My name is ...'"

    return None  

# Main function to get chatbot's response
def get_response(user_input):
    user_input = user_input.lower().strip()  # Normalize input

    # Check if user asked an exact question like "how are you?"
    if user_input in direct_questions:
        return random.choice(direct_questions[user_input])

    # Handle memory-based (context) input
    context_response = handle_context(user_input)
    if context_response:
        return context_response  # Return if context-based response is found

    # Match intent based on keyword patterns
    intent = get_intent(user_input)
    if intent:
        response = respond_to_intent(intent)  # Get random response for intent

        # Personalize response if name is known and it's a greeting
        if context["name"] and intent == "greeting":
            response += f" Nice to see you again, {context['name']}!"
        return response

    # Default fallback if no match
    return "I'm not sure I understand. Could you rephrase that?"

# Chat loop function to interact with user
def chat():
    print("ChatBot: Hello! What's your name?")
    print("Type 'bye' or 'exit' to end the chat.")

    while True:
        user_input = input("You: ")  # Take input from user

        if user_input.strip() == "":  # Ignore empty input
            print("ChatBot: Please say something!")
            continue

        # Exit conditions
        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            print("ChatBot: Goodbye! Take care.")
            break

        # Get chatbot's response and print it
        response = get_response(user_input)
        print("ChatBot:", response)

# Start chatbot
chat()
