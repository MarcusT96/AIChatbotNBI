# Yoda's Galactic Feast Chatbot 🤖🍽️

Welcome, young Padawan! This project demonstrates three different approaches to building an interactive chatbot using Python and LangChain. Each implementation showcases different architectural patterns and capabilities while maintaining Yoda's iconic speaking style.

## 🤖 Agent Implementations

### 1. Simple RAG Chain (`main.py`)
A straightforward implementation using Retrieval-Augmented Generation (RAG):
- Uses vector store for semantic search over restaurant information
- Maintains conversation history for context
- Simple linear chain: Query → Retrieve → Generate Response
- Best for basic Q&A about the restaurant

### 2. Graph-Based Agent (`agent.py`)
A more sophisticated implementation using LangGraph:
- Structured as a directed graph of operations
- Separate nodes for retrieval and response generation
- Clear separation of concerns between context gathering and response generation
- Better for complex interactions requiring multiple steps

### 3. ReAct Agent (`react_agent.py`)
The most advanced implementation using the ReAct (Reasoning and Action) pattern:
- Tool-using agent that can perform specific actions
- Supports multiple functions:
  - Making reservations
  - Checking daily specials
  - Star Wars trivia Q&A
  - Answer verification
- Maintains conversation state between interactions
- Best for task-oriented conversations requiring specific actions

## 🎯 Learning Objectives

Through this project, you'll learn about:
- Different chatbot architectures (Chain, Graph, ReAct)
- Working with Large Language Models (LLMs)
- Using vector stores for semantic search
- Implementing conversation state management
- Tool-based agents and action handling
- Managing environment variables
- Creating interactive command-line interfaces

## 🛠️ Technologies Used

- **Python**: The primary programming language
- **LangChain**: Framework for building LLM applications
- **LangGraph**: For building graph-based agents
- **Anthropic Claude**: Advanced LLM for natural language processing and better at tool calling
- **HuggingFace**: For text embeddings
- **python-dotenv**: For environment variable management
- **OpenAI apikey**: Go to https://platform.openai.com/ and create an account to get an api key - you need to add payment method to the account and top it up with credits to use. 

## 📋 Prerequisites

- Python 3.10 or higher
- Basic understanding of Python programming
- API keys for:
  - Anthropic (for Claude)
  - Groq (optional, for alternative model)

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AIchatbotNBI
```

### 2. Create a Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate the virtual environment
# For Linux/MacOS:
source venv/bin/activate

# For Windows (CMD):
.\venv\Scripts\activate.bat

# For Windows (PowerShell):
.\venv\Scripts\activate.ps1

# For Windows with Git Bash:
source venv/Scripts/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root and add your API keys:
```
ANTHROPIC_API_KEY="your_anthropic_api_key_here"
GROQ_API_KEY="your_groq_api_key_here"  # Optional
```

### 5. Prepare Your Data
The chatbot uses `yoda_galactic_feasts.txt` for restaurant information. You can modify this file to customize the bot's knowledge base.

### 6. Run the Chatbot
Choose which implementation to run:
```bash
# For simple RAG implementation
python main.py

# For graph-based agent
python agent.py

# For ReAct agent with tools
python react_agent.py
```

## 🧠 How It Works

### RAG Chain (`main.py`)
```python
chain = {
    "context": retriever,
    "question": RunnablePassthrough(),
    "chat_history": RunnableLambda(lambda x: format_history(message_history))
} | prompt | llm | StrOutputParser()
```
This implementation uses a simple chain that retrieves relevant context and generates responses.

### Graph Agent (`agent.py`)
```python
graph_builder = StateGraph(State)
graph_builder.add_node("rag_search", rag_search)
graph_builder.add_node("answer", answer)
```
The graph-based implementation separates the previous chain operations into distinct nodes for better control flow. Possible to add more nodes to the graph and conditionally execute nodes based on the state.

### ReAct Agent (`react_agent.py`)
```python
agent = create_react_agent(
    model=model,
    tools=[trivia_question, check_answer, make_reservation, get_todays_special],
    prompt=prompt
)
```
The ReAct implementation combines an LLM with tools for specific actions. The ReAct agent acts as a standalone agent that can call different tools depending on the user's request and context. 

## 🔍 Key Concepts

1. **RAG (Retrieval-Augmented Generation)**: Enhances responses with relevant context
2. **Graph-Based Agents**: Structured flow of operations
3. **ReAct Pattern**: Combines reasoning and action in a single agent
4. **Vector Stores**: Semantic search for relevant information
5. **Tool Use**: Specific functions an agent can perform
6. **State Management**: Maintaining conversation context


## 🛠️ Customization Options

1. Modify the prompts to change the bot's personality
2. Add new tools to the ReAct agent
3. Extend the graph structure with new nodes
4. Adjust the RAG implementation for different retrieval strategies

## 📚 Learning Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [ReAct Pattern](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/)

## 🤝 Contributing

Feel free to fork this project and customize it for your own learning! Some ideas for extensions:
- Add support for multiple restaurants
- Implement a web interface
- Add more sophisticated conversation handling
- Integrate with a database for persistent storage

## ⚠️ Common Issues and Solutions

1. **ModuleNotFoundError**: Make sure you've activated your virtual environment and installed all requirements
2. **API Key Error**: Check that your `.env` file is properly configured
3. **Memory Issues**: Reduce chunk size if processing large documents

## 📊 Monitoring and Debugging

This project uses LangSmith for monitoring and debugging the LLM application. LangSmith provides:

1. **Trace Visualization**: See how your chains and agents process requests
2. **Performance Monitoring**: Track latency, token usage, and costs
3. **Debug Interface**: Inspect intermediate steps and outputs

To access these features:
1. Sign up for LangSmith at [smith.langchain.com](https://smith.langchain.com/)
2. Get your API key from the LangSmith dashboard
3. Add the key and other LangSmith configurations to your `.env` file
4. Visit the LangSmith dashboard to monitor your application

## 🌐 Connecting a Frontend

### Running the API Server

1. Start the API server with uvicorn:
```bash
# Development mode with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend Integration

The API supports CORS and can be connected to any frontend framework. Here are examples using different technologies:

#### JavaScript/Fetch
```javascript
async function chatWithYoda(message) {
    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                thread_id: 'your-conversation-id (example: "thread1")'
            })
        });
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error:', error);
    }
}
```

#### React/Axios
```javascript
import axios from 'axios';

const YodaChat = () => {
    const sendMessage = async (message) => {
        try {
            const response = await axios.post('http://localhost:8000/chat', {
                message: message,
                thread_id: 'your-conversation-id'
            });
            return response.data.response;
        } catch (error) {
            console.error('Error:', error);
        }
    };
};
```

#### Python/Requests
```python
import requests

def chat_with_yoda(message):
    try:
        response = requests.post(
            'http://localhost:8000/chat',
            json={
                'message': message,
                'thread_id': 'your-conversation-id'
            }
        )
        return response.json()['response']
    except Exception as e:
        print(f"Error: {e}")
```

### API Endpoints

- `GET /` - Welcome endpoint
- `POST /chat` - Main chat endpoint
  - Request body:
    ```json
    {
        "message": "Your message here",
        "thread_id": "optional-conversation-id"
    }
    ```
  - Response:
    ```json
    {
        "response": "Yoda's response",
        "thread_id": "conversation-id"
    }
    ```
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Development Tools

The API comes with several development tools:

1. **Swagger UI** (`/docs`): Interactive API documentation and testing
2. **ReDoc** (`/redoc`): Alternative API documentation
3. **CORS support**: Enabled for all origins in development
4. **Auto-reload**: Available in development mode

### Security Considerations

Make sure to configure CORS properly in `app.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["your-frontend-domain.com"], # Replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
