import nltk
from nltk.chat.util import Chat, reflections

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1! How can I help you today?",]
    ],
    [
        r"what is your name?",
        ["My name is ChatBot. You can call me Bot.",]
    ],
    [
        r"how are you?",
        ["I'm doing well, thank you!", "I'm a computer program, so I don't have feelings, but thanks for asking!"]
    ],
    [
        r"(hi|hello|hey)",
        ["Hello!", "Hi there!", "How can I assist you?"]
    ],
    [
        r"quit",
        ["Goodbye! Have a great day!", "It was nice talking to you!"]
    ],
    [
        r"(.*) weather (.*)",
        ["I can't check real-time weather, but you can try a weather website!",]
    ],
    [
        r"thank you|thanks",
        ["You're welcome!", "No problem!", "Anytime!"]
    ],
    [
        r"(.*) (age|old) (.*)",
        ["I'm a computer program, I don't have an age!",]
    ],
    [
        r"what can you do?",
        ["I can chat with you, answer basic questions, and try to help with simple tasks!",]
    ],
]

def chatbot():
    print("ChatBot: Hi! I'm your basic chatbot. Type 'quit' to exit.")
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    nltk.download('punkt')
    chatbot()