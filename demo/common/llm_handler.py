from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Type
from demo.demo_tools import *
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.llms import Tongyi
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain.globals import set_verbose, set_debug

tongyi_llm = Tongyi()

stream_llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus",
        # 通过以下设置，在流式输出的最后一行展示token使用信息
        stream_options={"include_usage": True}
        )

def get_tool_schema(tool):
    """获取工具的 schema 定义"""
    schema = {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
        }
    }
    
    if hasattr(tool, 'args_schema'):
        # 如果工具有 args_schema，使用它的 schema
        schema["function"]["parameters"] = tool.args_schema.schema()
    else:
        # 否则使用默认的空参数
        schema["function"]["parameters"] = {
            "type": "object",
            "properties": {},
            "required": []
        }
    
    return schema

normal_llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
    model_kwargs={
        "tool_choice": "auto",
        "tools": [get_tool_schema(tool) for tool in tools]
    }
)

def get_answer(message: str):
    messages = [
        {"role":"system","content":"You are a helpful assistant."},
        {"role":"user","content":message},
    ]
    response = stream_llm.stream(messages)
    for chunk in response:
        json_str = chunk.model_dump_json()
        # 使用 json.dumps 控制 ensure_ascii
        formatted_json = json.dumps(json.loads(json_str), indent=4, ensure_ascii=False)
        json_data = json.loads(json_str)
        print(json_data.get("content"), end="")
    print(" -- answer end --")

def get_struct_answer(message: str, class_type: Type[TypedDict]):
    structured_llm = stream_llm.with_structured_output(class_type)
    for chunk in structured_llm.stream(message):
        print(chunk)

def teach_ai(input, examples, prompt, class_type: Type[TypedDict]):
    structured_llm = normal_llm.with_structured_output(class_type)
    few_shot_structured_llm = prompt | structured_llm
    for chunk in few_shot_structured_llm.stream({
        "input": input,
        "examples": examples,
        "stream": True,
        "stream_options": {
            "max_tokens": 100
        }
    }):
        print(chunk)

def answer_by_tool(query: str):
    llm_with_tools = normal_llm.bind_tools(tools)
    messages = [HumanMessage(query)]
    ai_msg = llm_with_tools.invoke(messages)
    print(ai_msg.tool_calls)
    messages.append(ai_msg)
    print("message_ai_msg", messages)
    for tool_call in ai_msg.tool_calls:
        selected_tool = {"add": add, "multiply": multiply, "gettweet": getTweet}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)
    print("message_tool_msg", messages)
    response = llm_with_tools.invoke(messages)
    print("message_response", response)

async def query_stream(query: str):
    chunks = []
    async for chunk in normal_llm.astream(query):
        chunks.append(chunk)
        print(chunk.content, end="|", flush=True)
    print()
    print(chunks[0] + chunks[1] + chunks[2])

async def parser_stream(query: str):
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
    parser = StrOutputParser()
    chain = prompt | normal_llm | parser

    async for chunk in chain.astream({"topic": query}):
        print(chunk, end="|", flush=True)




def _extract_country_names(inputs):
    """A function that does not operates on input streams and breaks streaming."""
    if not isinstance(inputs, dict):
        return ""

    if "countries" not in inputs:
        return ""

    countries = inputs["countries"]

    if not isinstance(countries, list):
        return ""

    country_names = [
        country.get("name") for country in countries if isinstance(country, dict)
    ]
    return country_names

async def _extract_country_names_streaming(input_stream):
    """A function that operates on input streams."""
    country_names_so_far = set()

    async for input in input_stream:
        if not isinstance(input, dict):
            continue

        if "countries" not in input:
            continue

        countries = input["countries"]

        if not isinstance(countries, list):
            continue

        for country in countries:
            name = country.get("name")
            if not name:
                continue
            if name not in country_names_so_far:
                yield name
                country_names_so_far.add(name)
async def get_country(query: str):
    chain = (
        normal_llm | JsonOutputParser() | _extract_country_names
    )  # Due to a bug in older versions of Langchain, JsonOutputParser did not stream results from some models
    async for text in chain.astream(query):
        print(text, flush=True)

    chain = (
        normal_llm | JsonOutputParser() | _extract_country_names_streaming
    )  # Due to a bug in older versions of Langchain, JsonOutputParser did not stream results from some models
    async for text in chain.astream(query):
        print(text, end="|", flush=True)

def tongyi_get_answer(query: str):
    response = tongyi_llm.invoke(query)
    print(response)

def debug_llm():
    tools = [TavilySearchResults(max_results=1)]
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant.",
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Construct the Tools agent
    agent = create_tool_calling_agent(normal_llm, tools, prompt)

    set_debug(True)
    set_verbose(True)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    response = agent_executor.invoke(
        {"input": "Who directed the 2023 film Oppenheimer and what is their age in days?"}
    )
    print(response)

