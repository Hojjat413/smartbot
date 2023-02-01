
import random
import re
import openai

# Use the OpenAI API to generate responses based on the context of the conversation
openai.api_key = "YOUR_API_KEY"
def generate_response(prompt):
    completions = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=20, n=1, stop=None, temperature=0.7)
    message = completions.choices[0].text
    return message.strip()

# A list of pre-defined responses that the chatbot can use
responses = [
    "Hello, how are you today?",
    "Good morning/afternoon/evening, how are you?",
    "Hi, how's it going?",
    "What's up?",
    "I'm doing great, thank you for asking. How can I help you today?",
    "I'm doing well, thanks for asking. Is there anything specific you would like to talk about?",
    "I'm doing well. How has your day been so far?",
]

# A list of conversation history
# A list of conversation history to use for training the chatbot
conversation_history = [
    "Hello, How are you.",
    "Good to see you, how are you doing?",
    "It's great to see you. How's your day been?",
    "I'm glad to see you. How's everything going?",
    "I'm happy to see you. How's your day going?",
    "It's good to see you. How are you doing?",
    "I hope this message finds you well. How have you been?",
    "Hello, how have you been?",
    "I'm doing well, thanks for asking. How about you?",
    "I'm doing well too. Do you have any plans for the weekend?",
    "Not yet, do you have any suggestions?",
    "We could go for a hike or see a movie. What do you think?",
    "A hike sounds like fun. Where do you want to go?",
    "How about Mount Tamalpais? It has some great trails with beautiful views.",
    "That sounds great! When do you want to go?",
    "How about Saturday at 10am?",
    "Saturday at 10am works for me. See you then!",
    "I'm looking forward to it. See you on Saturday!",
]

# Pre-process the conversation history by tokenizing and lowercasing the text
conversation_history = [re.findall(r'\w+', text) for text in conversation_history]
conversation_history = [[word.lower() for word in text] for text in conversation_history]

# Create a bag-of-words model from the conversation history
word_counts = {}
for text in conversation_history:
    for word in text:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

def chatbot():
  # Continuously get user input and respond until the user says "goodbye"
  while True:
    # Get user input
    user_input = input("You: ")

    # Check if the user input is "goodbye"
    if user_input.lower() == "goodbye":
      print("Chatbot: Goodbye! It was nice talking to you.")
      break

    # If the user input is not "goodbye", use the bag-of-words model and the OpenAI API
    # to generate a response based on the user input
    else:
      user_input = re.findall(r'\w+', user_input)
      user_input = [word.lower() for word in user_input]

      # Find the response with the highest number of common words with the user input
      best_response = None
      max_common_words = 0
      for text in conversation_history:
          common_words = len(set(text) & set(user_input))
          if common_words > max_common_words:
              max_common_words = common_words
              best_response = text

      # If no response was found, use the OpenAI API to generate a response
      if best_response is None:
          response = generate_response(user_input)
      else:
          response = ' '.join(best_response)
      # If the OpenAI API generates an empty response, use a pre-defined response
      if response == "":
          response = random.choice(responses)

      print("Chatbot: " + response)

# Run the chatbot
chatbot()
