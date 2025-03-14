from agents import Agent, Runner, WebSearchTool, RunContextWrapper, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel

#Don't forget to pip install "openai-agents" package

class UserContext(BaseModel):
    user_id: str
    name: str
    purchase_history: list[str]

@function_tool
def purchase_history(context: RunContextWrapper[UserContext], user:str) -> str:
    """Get the user's purchase history."""
    return f"Your purchase history is {context.context.purchase_history}"

@function_tool
def add_purchase(context: RunContextWrapper[UserContext], item: str) -> str:
    """
    Add a new purchase to the user's purchase history.
    """
    context.context.purchase_history.append(item)
    return f"You have purchased {item}"

agent = Agent(
    name="websearch-agent",
    tools=[WebSearchTool(), purchase_history, add_purchase],
    instructions="You are a helpful customer assistant. You help customers to know what they have purchased earlier and help them search the web and add new items to their purchase history",
    model="gpt-4o-mini"
)


async def main():

    context = UserContext(user_id="1", name="John Doe", purchase_history=["Laptop", "Phone", "Nvidia 4090"])
    result = Runner.run_streamed(agent, "What have I bought? I want to buy a new Nvidia 4090, what does it cost today? Please add one to my purchase history", context=context)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    print(context.purchase_history)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 