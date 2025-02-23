#Import the agent library
from smolagents import CodeAgent,LiteLLMModel,DuckDuckGoSearchTool
from smolagents import tool


model_name="ollama_chat/llama3.2"
#Use LiteLLMModel to load ollama api
model =LiteLLMModel(
    model_id=model_name,
    api_base="http://localhost:11434",
    #api_key="your-api-key",
    num_ctx=8192,
)

# @tool
# def duck_search(search_query: str) -> str:
#     """
#     Allows you to search the web. Returns a string representation of the result.
#     """
#     search_tool = DuckDuckGoSearchTool(search_query)
#     return

#create the agent
agent = CodeAgent(
    tools=[],
    model=model,
    add_base_tools=True,
)

query=input("Enter your query: ")

agent.run(query)
#agent.run("Can you give me the name of the client who got the most expensive receipt?")
