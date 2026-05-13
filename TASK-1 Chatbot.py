def simple_chatbot():
    print("Chatbot: Hello! I'm a rule-based bot. Type 'exit' to end our chat.")
    
    while True:
        # 1. Get user input and normalize it (lowercase)
        user_input = input("You: ").lower().strip()

        # 2. Define the rules
        if user_input == "exit":
            print("Chatbot: Goodbye! Have a great day.")
            break
        
        elif "hello" in user_input or "hi" in user_input:
            print("Chatbot: Hey there! How can I help you today?")
            
        elif "your name" in user_input:
            print("Chatbot: I'm Mini-Bot, your friendly Python script.")
            
        elif "how are you" in user_input:
            print("Chatbot: I'm functioning within normal parameters. Thanks for asking!")
            
        elif "weather" in user_input:
            print("Chatbot: I don't have a window, but it looks like 1s and 0s from here.")
            
        # 3. The fallback (if no rules match)
        else:
            print("Chatbot: I'm sorry, I didn't quite catch that. Could you try rephrasing?")

# Run the chatbot
if __name__ == "__main__":
    simple_chatbot()