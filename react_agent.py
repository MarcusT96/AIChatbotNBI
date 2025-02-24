# Import necessary libraries
# langgraph.prebuilt: Provides pre-built agent structures for conversation flows
# langchain_core.messages: Contains message types for chat interactions
# langchain_anthropic: Interface for the Anthropic Claude AI model
# dotenv: For loading environment variables from a .env file
# random: For selecting random trivia questions
# MemorySaver: Helps maintain conversation state between interactions
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
import random
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables from .env file
load_dotenv()

# Initialize the AI model (Claude 3.5 Sonnet)
# This is the main language model that will process user inputs and generate responses
# temperature: Controls randomness in responses (0.0 = deterministic, 1.0 = more randomm 2.0 = complete randomness)
model = ChatAnthropic(
    model_name="claude-3-5-sonnet-20241022",
    temperature=0.6,
    api_key=os.getenv("ANTHROPIC_API_KEY")  # Get API key from environment variables
)

# Initialize the OpenAI model (GPT-4o)
# This is the main language model that will process user inputs and generate responses
# temperature: Controls randomness in responses (0.0 = deterministic, 1.0 = more random, 2.0 = complete randomness)
#model = ChatOpenAI(
  #  model_name="gpt-4o-mini",
  #  temperature=0.6,
  #  api_key=os.getenv("OPENAI_API_KEY")  # Get API key from environment variables
#)


# Database of Star Wars trivia questions and answers
# Structured as a dictionary where each entry has a unique key and contains:
# - question: The trivia question to ask
# - answer: The correct answer to the question
TRIVIA_DATA = {
    "yoda_species": {
        "question": "What species is Yoda?",
        "answer": "Unknown - his species has never been named"
    },
    "yoda_exile": {
        "question": "On which swamp planet did Yoda live in exile?",
        "answer": "Dagobah"
    },
    "millennium_falcon": {
        "question": "What is the name of Han Solo's corellian freighter?",
        "answer": "Millennium Falcon"
    },
    "clone_army": {
        "question": "Which planet was the clone army secretly created on?",
        "answer": "Kamino"
    },
    "sith_lord": {
        "question": "Who was the Sith Lord secretly ruling the Galactic Senate?",
        "answer": "Darth Sidious/Palpatine"
    },
    "first_order_weapon": {
        "question": "What was the First Order's planet-sized superweapon called?",
        "answer": "Starkiller Base"
    },
    "republic_capital": {
        "question": "What was the capital planet of the Galactic Republic?",
        "answer": "Coruscant"
    }
}

# The main prompt that defines the chatbot's personality and behavior
# This tells the AI model how to act (as Yoda) and when to use different tools
prompt = """
You are Yoda, the wise Jedi Master, running your restaurant 'Yoda's Galactic Feast'. Speak in Yoda's style - with inverted sentence structure, hmmmm.

IMPORTANT: Keep your responses short and focused. Do not ramble or add unnecessary information.

Response Guidelines:

1. For greetings (hi, hello, etc.):
   - Respond with a simple welcome
   - Example: "Welcome, young one, hmmmm." or "Greetings, to Yoda's Galactic Feast, you have come."
   - DO NOT add random information about the menu or restaurant unless asked

2. When to use tools:
   - make_reservation: ONLY when customer explicitly asks to make a reservation, make sure to ask what time and date and how many people before you call the tool
   - get_todays_special: ONLY when customer asks about todays special, when you have used the tool you can tell the customer what the special is
   - trivia_question: ONLY when customer specifically asks for trivia or Star Wars knowledge
   - check_answer: When customer attempts to answer a trivia question

3. Tool response format:
   - Use the tool
   - Give a single brief comment about the result
   - Wait for customer's next question

Remember:
- Keep responses SHORT and ON-TOPIC
- Don't volunteer information that wasn't asked for
- Use "hmmmm" sparingly
- Speak in Yoda's inverted style, but keep it simple
"""

# Tool Functions
# These are the actions our chatbot can perform when requested

def trivia_question() -> str:
    """Get a random Star Wars trivia question.
    Returns a randomly selected question from our trivia database."""
    trivia = random.choice(list(TRIVIA_DATA.values()))
    return trivia["question"]

def check_answer(answer: str) -> str:
    """Check if a user's answer matches the correct answer for any trivia question.
    Performs case-insensitive partial matching to be user-friendly.
    Returns a success or failure message."""
    for trivia in TRIVIA_DATA.values():
        if answer.lower() in trivia["answer"].lower():
            return f"Correct! {trivia['answer']}"
    return "Incorrect, that answer is. Try again, you must."
    
def make_reservation(num_of_people: int, time: str, date: str) -> str:
    """Handle restaurant reservations.
    Takes number of people, time, and date as parameters.
    Returns a confirmation message."""
    return f"Reservation made successfully for {num_of_people} people at {time} on {date}"

def get_todays_special() -> str:
    """Retrieve today's special menu items.
    Returns a string containing the day's special menu items."""
    return "todays special: Taco, Burrito, Nachos, and a drink"

# Create the ReAct agent
# This combines the AI model, tools, and prompt into a functional chatbot
# - model: The AI model that processes inputs and generates responses
# - tools: List of functions the agent can use
# - prompt: Instructions for how the agent should behave
# - checkpointer: Helps maintain conversation state
agent = create_react_agent(
    model=model,
    tools=[trivia_question, check_answer, make_reservation, get_todays_special],
    prompt=prompt,
    checkpointer=MemorySaver()
)

def chat():
    """Main chat loop function.
    Handles:
    1. Displaying welcome message
    2. Getting user input
    3. Processing input through the agent
    4. Displaying the agent's response
    5. Continuing until user quits"""
    print("\nWelcome to Yoda's Galactic Feast! Ask about reservations, menu, or Star Wars trivia. Type 'quit' to exit.\n")
    
    while True:
        # Get user input
        user_input = input("\nUser: ")
        
        # Check for quit command
        if user_input.lower() in ["quit", "exit", "q"]:
            print("\nMay the Force be with you!")
            break
        
        # Process user input through the agent
        # - messages: List containing the user's message
        # - config: Configuration for the conversation thread
        result = agent.invoke({"messages": [HumanMessage(content=user_input)]}, config={"configurable": {"thread_id": "thread2"}})
        
        # Extract and display the agent's response
        # We only want to show the last message in the conversation
        if result.get("messages"):
            last_message = result["messages"][-1]
            if hasattr(last_message, "content"):
                print("\nYoda:", last_message.content)


# Only run the chat function if this file is run directly
if __name__ == "__main__":
    chat()