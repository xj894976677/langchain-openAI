import os

import tweepy
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Callable, List, Any


# 创建一个工具类
class TwitterTool(Tool):
    bearer_token: str
    client: tweepy.Client = None

    def __init__(self, name: str, func: Callable, description: str, **kwargs):
        super().__init__(name=name, func=func, description=description, **kwargs)
        self.client = tweepy.Client(bearer_token=self.bearer_token)

    def run(self, username: str) -> list[Any]:
        print("yes run twitter tools")
        try:
            # 获取用户的 ID
            user = self.client.get_user(username=username)
            if user.data:
                tweets = self.client.get_users_tweets(id=user.data.id, max_results=5)  # 获取用户的最新推文
                print("twitter tool tweets is :", tweets)
                return [tweet.text for tweet in tweets.data] if tweets.data else []
            else:
                print(f"用户 {username} 不存在")
                return []
        except Exception as e:
            print(f"获取推文时出错: {e}")


twitter_tool = TwitterTool(
    name="get_tweets_by_name",  # 名称
    func=TwitterTool.run,  # 工具的功能函数，通常是工具的调用方法
    description="用于获取elonmusk最新的一条帖文是什么内容",  # 工具的描述
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
)
