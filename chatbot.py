# import all libraries
import nltk
from nltk.chat.util import Chat, reflections
import requests
import wikipediaapi

# create the wikipedia API object
wiki_wiki = wikipediaapi.Wikipedia("English")


# chatbot function initialises the chatbot to prompt a conversation
def chatbot():
    print('TYPE "hi" to start chatting or "bye" to exit')
    print("Chatbot: Hello. Im Chatbot.")

    # create chatbot
    chat = Chat(pairs, reflections)

    # overrides the converse method of nltk to customise
    # input processing for search function
    while True:
        user_input = input("Me: ").lower()  # turns user input to lowercase for processing
        # check if user wants to terminate programme
        if user_input == "bye" or user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        # checks for phrase to initialise search_wiki
        elif user_input.startswith("search for "):
            query = user_input[len("search for "):]  # extracts the query
            result = search_wiki(query)
            print(f"Chatbot: {result}")

        # checks for alternative phrasing for search_wiki prompt
        elif user_input.startswith("who is "):
            query = user_input[len("who is "):]  # extracts the query
            result = search_wiki(query)
            print(f"Chatbot: {result}")

        # use pairs to respond to user input
        else:
            response = chat.respond(user_input)
            print(f"Chatbot: {response}")


def get_fact():
    api_url = "http://numbersapi.com/random/trivia"
    try:
        response = requests.get(api_url)
        fact = response.text  # True enables a safe filter to filter out all inappropriate, political or NSFW facts
        return fact
    except Exception:
        return "Sorry, I can't think of anything interesting right now."


# uses external API to tell a joke
def get_joke():
    api_url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(api_url)
        joke = response.json()
        return f"{joke['setup']}, {joke['punchline']}"

    except Exception:
        return "Sorry, you can't put me on the spot like that."


# searches wikipedia using wikipedia API
def search_wiki(query):
    try:
        page_py = wiki_wiki.page(query)
        if page_py.exists():
            return "\n " + page_py.text[:550]  # return the first 500 characters of the wiki article
        else:
            return "Sorry. I couldn't find any information on " + query + "."

    except Exception:
        return "Sorry. I'm finding trouble answering that. Can we move on?'"


# containing all generic potential input lines and responses
pairs = [
    ["hi|hello|hey", ["Hi! How can I assist you today?", "Hi! How are you today?", "Hello! What is your name?"]],
    ["(.*)great|(.*)fine|(.*)super|(.*)ok|(.*)okay|(.*)good", ["I'm glad to hear that :), How may I help?"]],
    ["(.*)bad|not so well|(.*)horrible|(.*)terrible", ["I'm so sorry to hear that :(, How may I help you?",
                                                       "Is there some way I could help you with to make you feel better?"]],
    ["yes", ["How may i help?"]],
    ["how are you(.*)", ["I'm great. How about you?", "I'm great! Thanks for asking."]],
    ["who are you|(.*)your name", ["I'm steve. But you can call me Chatbot!"]],
    ["my name is (.*)|im (.*)", ["Hi %1, nice to meet you."]],
    ["what can you do|tell me about yourself", ["I'm happy to tell you more about myself! I can search wikipedia for you if you just say 'search for...', "
                                                "I can tell you jokes, random facts and I'm more than happy to have a chat if you simply want to talk!"]],
    ["thanks|thank you|(.*)helpful", ["No problem! I'm glad I could help."]],
    ["(.*)no|(.*)wrong", ["I'm sorry", "Sorry. Would you mind phrasing that differently so I can help?"]],
    ["(.*)random fact|(.*)fact", ["Here's a random fact of the day: " + get_fact()]],
    ["tell me a joke|(.*)joke", ["Let me think..." + get_joke(), get_joke()]],
    [" ", ["Why so quiet?"]],
    ["default|(.*)", ["I'm not sure how to respond to that.", "Would you mind rephrasing that?", "Sorry, I don't understand"]]
]

# call chatbot
chatbot()
