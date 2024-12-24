from langchain_openai import ChatOpenAI
from requests_toolbelt.multipart.encoder import reset
from langchain_core.output_parsers import PydanticToolsParser
from typing_extensions import Annotated, TypedDict, Optional
from langchain_core.messages import HumanMessage
from typing import Type
import os
import json
from models import Joke
from tools import *

stream_llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus",
        # 通过以下设置，在流式输出的最后一行展示token使用信息
        stream_options={"include_usage": True}
        )
normal_llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus"
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
        selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)
    print("message_tool_msg", messages)
    response = llm_with_tools.invoke(messages)
    print("message_response", response)