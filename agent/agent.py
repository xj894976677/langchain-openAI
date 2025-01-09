from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from common.llm_handler import normal_llm
from langgraph.checkpoint.memory import MemorySaver

from demo_tools import tools
from tools.math import math_tool
from tools.twitter import twitter_tool

search = TavilySearchResults(max_results=2)
search_results = search.invoke("what is the weather in SF")
# If we want, we can create other tools.
# Once we have all the tools we want, we can put them in a list that we will reference later.

memory = MemorySaver()
agent_executor = create_react_agent(normal_llm, tools, checkpointer=memory)

async def getAdd():
    config = {"configurable": {"thread_id": "abc123"}}
    # await answer(config, "hi im bob!")
    # await answer(config, "what is my name?")
    await answer(config, "1+2的结果是什么？")


async def getTwitter():
    config = {"configurable": {"thread_id": "abc123"}}
    # await answer(config, "hi im bob!")
    # await answer(config, "what is my name?")
    await answer(config, "elonmusk 最新的一条帖文是什么内容？")
    await answer(config, "从elonmusk 最新的帖文能看出什么东西？")


async def answer(config, query):
    async for event in agent_executor.astream_events(
        {"messages": [HumanMessage(content=query)]}, version="v1", config=config
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(content, end="|")

        # 处理工具调用
        if "tool_calls" in event["data"]:
            for tool_call in event["data"]["tool_calls"]:
                # 识别工具并处理返回结果
                tool_name = tool_call["name"]
                if tool_name == "add_two_number":
                    arguments = tool_call["arguments"]
                    result = math_tool.run(**arguments)
                    print(f"工具 {tool_name} 返回结果: {result}")