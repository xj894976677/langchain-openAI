import os

import tweepy
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Callable, List, Any


# 创建一个工具类
class MathTool(Tool):
    bearer_token: str
    client: tweepy.Client = None

    def __init__(self, name: str, func: Callable, description: str, **kwargs):
        super().__init__(name=name, func=func, description=description, **kwargs)

    def run(self, number_one: int,  number_two: int):
        print("yes run MathTool")
        return number_one + number_two


math_tool = MathTool(
    name="add_two_number",  # 名称
    func=MathTool.run,  # 工具的功能函数，通常是工具的调用方法
    description="返回两个数字相加的结果",  # 工具的描述
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
)
