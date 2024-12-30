from langchain.chains.llm import LLMChain
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from llm_handler import normal_llm, tongyi_llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import SystemMessage, trim_messages

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

messages = [
    SystemMessage(content="you're a good assistant"),
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]

def call_model(state: State):
    trimmed_messages = getTrimmer().invoke(state["messages"])
    prompt = prompt_template.invoke(
        {"messages": trimmed_messages, "language": state["language"]}
    )
    response = normal_llm.invoke(prompt)
    return {"messages": [response]}

# Async function for node:
async def call_model_async(state: State):
    prompt = await prompt_template.ainvoke(state)
    response = await normal_llm.ainvoke(prompt)

    return {"messages": response}

async def async_chat(query:str):
    # Define graph as before:
    workflow = StateGraph(state_schema=State)
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model_async)
    app = workflow.compile(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "abc123"}}
    language = "Chinese"

    query = "What's my name?"
    input_messages = [HumanMessage(query)]
    # Async invocation:
    output = await app.ainvoke({"messages": input_messages, "language": language}, config)
    output["messages"][-1].pretty_print()

def chat():
    # Define a new graph
    workflow = StateGraph(state_schema=State)
    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "abc123"}}

    language = "English"
    # query = "What's my name?"
    #
    # input_messages = messages + [HumanMessage(query)]
    # output = app.invoke({"messages": input_messages, "language": language}, config)
    # output["messages"][-1].pretty_print()

    query = "What math problem did I ask?"
    input_messages = messages + [HumanMessage(query)]
    output = app.invoke({"messages": input_messages, "language": language}, config)
    output["messages"][-1].pretty_print()

def getTrimmer():
    trimmer = trim_messages(
        max_tokens=50,
        strategy="last",
        token_counter=tongyi_llm,
        include_system=True,
        allow_partial=False,
        start_on="human",
    )

    print(trimmer.invoke(messages))
    return trimmer