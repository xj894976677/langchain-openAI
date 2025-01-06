import json
import os
from typing import List, Any

import tweepy
from typing_extensions import Annotated, TypedDict
from pydantic import BaseModel, Field
from langchain_core.tools import tool
@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b
@tool
def getTweet(username: str) -> list[Any]:
    """
        获取指定用户最新的5条推文。按照发布时间倒序排列,用,分割
        :param username: 用户名
        :return: 最新推文内容
        """
    print("yes run twitter tools")
    client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))
    try:
        # 获取用户的 ID
        user = client.get_user(username=username)
        if user.data:
            tweets = client.get_users_tweets(id=user.data.id, max_results=5)  # 获取用户的最新推文
            print("twitter tool tweets is :", tweets)
            # return tweets.data[0].text
            return json.dumps([tweet.text for tweet in tweets.data] if tweets.data else [])
        else:
            print(f"用户 {username} 不存在")
            return []
    except Exception as e:
        print(f"获取推文时出错: {e}")
        return json.dumps(["hello every ony,are you ok?", "how are you", "hahahhahaha", "wow it is nice" , "i like this"])
tools = [add, multiply, getTweet]

