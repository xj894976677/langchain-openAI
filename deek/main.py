import os
from typing import Any, List, Optional
from datetime import datetime

from dotenv import load_dotenv
from dashscope import Generation
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

from twitter_tool import TwitterAPI
from deek_tool import DeekAPI

# 加载环境变量
load_dotenv()

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema.output import GenerationChunk

class QwenLLM(LLM):
    """阿里云 Qwen 模型的 LangChain 集成"""
    
    model_name: str = "qwen-turbo"
    temperature: float = 0.7
    api_key: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.api_key:
            self.api_key = os.getenv("DASHSCOPE_API_KEY")
            if not self.api_key:
                raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

    @property
    def _llm_type(self) -> str:
        return "qwen"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
        response = Generation.call(
            model=self.model_name,
            api_key=self.api_key,
            prompt=prompt,
            temperature=self.temperature,
            result_format='message',
            stream=False,
        )
        
        if response.status_code == 200:
            content = response.output.choices[0].message.content
            if run_manager:
                run_manager.on_llm_new_token(content)
            return content
        else:
            raise Exception(f"API 调用失败：{response.message}")

def create_llm():
    """创建 Qwen LLM 实例"""
    return QwenLLM()

class CustomCallbackHandler(BaseCallbackHandler):
    """自定义回调处理器，用于流式输出和格式化"""
    
    def __init__(self):
        self.text_buffer = ""
        self.current_thought = ""
        self.current_action = ""
        self.current_action_input = ""
    
    def on_llm_start(self, *args, **kwargs):
        print("正在思考...", end="", flush=True)
        self.text_buffer = ""
    
    def on_llm_new_token(self, token: str, **kwargs):
        self.text_buffer += token
        print(token, end="", flush=True)
    
    def on_llm_end(self, *args, **kwargs):
        if self.text_buffer.strip():
            print("\n")
    
    def on_tool_start(self, action: AgentAction, **kwargs):
        print(f"\n正在获取数据: {action.tool}")
        print(f"查询参数: {action.tool_input}\n")
    
    def on_tool_end(self, output: str, *args, **kwargs):
        print("数据获取成功\n")
    
    def on_agent_finish(self, finish: AgentFinish, **kwargs):
        print("\n" + "-" * 50)
        print("分析结果:")
        print("-" * 50)
        print(finish.return_values['output'])
        print("-" * 50 + "\n")

def create_agent():
    """创建一个能够使用工具的智能体"""
    llm = create_llm()
    
    # 创建 Twitter API 实例
    twitter_api = TwitterAPI()
    deek_api = DeekAPI()
    
    # 创建 Twitter 工具
    twitter_tool = Tool(
        name="获取推特推文",
        description="获取指定用户的最新推文。输入应为用户的推特用户名（可以带@或不带@）。返回数据将包含推文内容、发布时间等信息。",
        func=twitter_api.get_latest_tweet,
        return_direct=False
    )

    # 创建 Deek 工具
    deek_tweets_tool = Tool(
        name="GetDeekTweets",
        description="获取指定用户在 Deek 平台的最新推文。输入用户ID，返回该用户的推文列表。当需要查看用户发布的内容时使用。",
        func=lambda x: deek_api.getDeekTweets(x),
        return_direct=False
    )

    deek_followers_tool = Tool(
        name="GetDeekFollowers",
        description="获取指定用户在 Deek 平台的关注者信息。输入用户ID，返回当前用户的粉丝用户ID的列表。",
        func=lambda x: deek_api.getDeekFollowers(x),
        return_direct=False
    )

    # 创建回调处理器
    callbacks = [CustomCallbackHandler()]
    
    # 创建对话记忆
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # 创建自定义提示模板
    custom_prompt = """你是一个智能的数据分析助手。请记住以下规则：
        
        1. 基本规则
           - 必须始终使用中文与用户交流
           - 即使数据中包含英文内容，也要用中文描述和解释
        
        2. 工具使用规则
           - 当用户的问题需要多个步骤时，要依次使用不同的工具
           - 根据一个工具的返回结果，判断是否需要调用其他工具
           - 例如：先获取用户列表，再为每个用户获取具体内容
        
        3. 分析步骤
           - 先获取基本数据
           - 根据返回的数据判断是否需要获取更多信息
           - 对所有收集到的数据进行完整分析
        
        当你获取到数据时，请按以下结构用中文分析：
        
        1. 数据总览
           - 总条目数
           - 数据类型和结构
        
        2. 详细分析
           - 每条数据的关键内容
           - 时间信息（如果有）
           - 独特或有趣的观察
        
        3. 特定分析
           - 根据用户的具体问题进行相应分析
           - 如果数据中包含列表，请逐项分析
        
        注意：
        - 请保持分析的完整性和准确性
        - 仅在必要时才使用工具获取新数据
        - 根据工具返回的内容，以此调用后续的工具以获取全量的数据
        - 始终使用中文回答
        
        Human: {input}
        Assistant: 让我来帮你分析这个问题。
        
        {agent_scratchpad}
    """

    # 创建代理
    agent = initialize_agent(
        tools=[twitter_tool, deek_tweets_tool, deek_followers_tool],
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=False,
        callbacks=callbacks,
        memory=memory,
        agent_kwargs={
            "memory_prompts": [MessagesPlaceholder(variable_name="chat_history")],
            "input_variables": ["input", "chat_history", "agent_scratchpad"],
            "prefix": custom_prompt,
            "system_message": "你是一个中文数据分析助手。无论处理什么数据，都必须用中文回复。即使工具返回英文数据，也要用中文解释和分析。"
        }
    )
    
    return agent

def chat_loop():
    """与 Agent 进行持续对话的主循环"""
    agent = create_agent()
    print("\n✨ Deek 平台智能助手已启动")
    print("\n💡 我会始终使用中文与您交流")
    print("\n☕️ 输入 'quit' 或 'exit' 可以退出对话\n")
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n💬 请输入您的问题：")
            
            # 检查是否退出
            if user_input.lower() in ['quit', 'exit']:
                print("\n✨ 感谢使用，再见！")
                break
            
            # 调用 agent
            print("\n")
            agent.invoke(
                input={
                    "input": user_input
                }
            )
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\n✨ 感谢使用，再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}\n")

def main():
    chat_loop()

if __name__ == "__main__":
    main()
