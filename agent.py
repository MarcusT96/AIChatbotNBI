from typing import Annotated
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from typing_extensions import TypedDict
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Set up vector store
#embeddings_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large-instruct")
#OpenAI embeddings can also be used, declare "OPENAI_API_KEY" in .env file and uncomment the following line. You also need to pip install langchain-openai
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv("OPENAI_API_KEY"))
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
loader = TextLoader("yoda_galactic_feasts.txt")
document = loader.load()
chunks = text_splitter.split_documents(document)
vector_store = InMemoryVectorStore.from_documents(chunks, embeddings_model)
retriever = vector_store.as_retriever()

# Set up LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.6,
    api_key=os.getenv("GROQ_API_KEY")
)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    context: str

def rag_search(state: State) -> State:
    """Retrieve relevant context from the vector store"""
    if not state["messages"]:
        return {"context": ""}
    
    last_message = state["messages"][-1]
    
    docs = retriever.invoke(last_message.content)
    context = "\n".join(doc.page_content for doc in docs)
    return {"context": context}

def answer(state: State) -> State:
    """Generate a response using the LLM and context"""

    prompt = PromptTemplate.from_template("""You are Yoda from Star Wars, running your restaurant 'Yoda's Galactic Feast'.
Answer the question using the provided context. Speak in Yoda's tone of voice.
Answer in a conversational tone in plain text without quotes.
                                          

Context: {context}

Question: {question}
                                          
Answer:
""")
    
    last_message = state["messages"][-1]
    
    # Create the chain
    chain = prompt | llm
    
    # Generate response
    response = chain.invoke({
        "context": state["context"],
        "question": last_message.content
    })
    
    return {"messages": [response]}

# Create graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("rag_search", rag_search)
graph_builder.add_node("answer", answer)

# Add edges
graph_builder.add_edge(START, "rag_search")
graph_builder.add_edge("rag_search", "answer")
graph_builder.add_edge("answer", END)

# Compile graph
graph = graph_builder.compile()

def chat():
    """Run the interactive chat loop"""
    print("\nWelcome to Yoda's Galactic Feast Chat! Type 'quit' to exit.\n")
    
    state = {
        "messages": [],
        "context": ""
    }
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("\nMay the Force be with you!")
            break
        
        state["messages"].append(HumanMessage(content=user_input))
        result = graph.invoke(state)
        
        messages = result.get("messages", [])
        if messages:
            last_message = messages[-1]
            print("\nYoda:", last_message.content)
        

if __name__ == "__main__":
    chat()