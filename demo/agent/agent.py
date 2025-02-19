from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from demo.common.llm_handler import normal_llm

from demo.demo_tools import tools

# 创建系统提示词
system_prompt = """
你是一个智能助手，可以帮助用户完成各种任务。你有以下几个主要功能：
1. 基础数学运算
2. 获取Twitter用户的推文
3. 获取Deek平台用户的推文和关注者信息

请根据用户的输入，选择合适的工具来完成任务。如果需要多个步骤，请逐步执行。
始终用中文回答用户的问题。
"""

# 创建提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 创建 agent
agent = create_openai_functions_agent(normal_llm, tools, prompt)

# 创建 agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

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

async def deekTweet():
    config = {"configurable": {"thread_id": "abc123"}}
    # await answer(config, "hi im bob!")
    # await answer(config, "what is my name?")
    await answer(config, "2024092308494390712897 在deek平台发布的最近的100条帖文都是什么内容？")

async def deekFollowers():
    config = {"configurable": {"thread_id": "abc123"}}
    await answer(config, "2024092308494390712897 在deek平台发布的最近的100条帖文都是什么内容？")
    # await answer(config, "2024092308494390712897 在deek平台上的粉丝用户有哪些？这些用户最近都发了哪些帖文？")
    # await answer(config, "根据我的粉丝们发布的内容，帮我分析下未来我发布什么类型的文章会更受欢迎一些")

    while True:
        # 提示用户输入问题
        user_input = input("轮到你说话了：")

        if user_input.lower() == 'exit':
            print("退出程序...")
            break  # 如果用户输入 'exit'，退出循环

        # 调用 answer 函数并等待其执行
        await answer(config, user_input)
    # await answer(config, "hi im bob!")
    # await answer(config, "what is my name?")




async def answer(config, query):
    try:
        # 创建输入消息
        input_dict = {
            "input": query,
            "chat_history": [],  # 可以存储历史对话
        }
        
        # 执行 agent并获取结果
        async for chunk in agent_executor.astream(input_dict):
            if isinstance(chunk, str):
                print(chunk, end="")
            elif isinstance(chunk, dict) and "output" in chunk:
                print(chunk["output"], end="")
    except Exception as e:
        print(f"执行出错: {str(e)}")