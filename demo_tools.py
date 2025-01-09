import json
import os
from typing import List, Any

import requests
import tweepy
from typing_extensions import Annotated, TypedDict
from pydantic import BaseModel, Field
from langchain_core.tools import tool
@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    print("hello")
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

@tool
def getDeekTweet(username: str) -> str:
    """
        获取指定用户在deek平台的最新100条推文。按照发布时间倒序排列
        :param username: 用户名
        :return: 以json的形式返回100条推文内容
        """
    try:
        url = 'https://api.deek.network/v1/feed/wish/timeline'
        params = {
            'nextToken': '',
            'limit': 100,
            'customerId': '2024092308494390712897',
            'role': 'MAKER'
        }
        # 请求头
        headers = {
            'jwt_token': 'eyJraWQiOiI4dnVrYmYxbmxtdGo1ZGE2d3owcTJyeGk5c2hjcHkzNyIsInR5cCI6IkpXVCIsImFsZyI6IkVTMjU2In0.eyJzdWIiOiJ0YWxlbnQiLCJhdWQiOiIyMDI0MDkyMzA4NDk0MzkwNzEyODk3IiwidWlkIjoiMjAyNDA5MjMwODQ5NDM5MDcxMjg5NyIsIndzS2V5IjoiUEQ4bUtXTVQiLCJuYmYiOjE3MzYzMjI4NTksInVzZXJfaWQiOiIyMDI0MDkyMzA4NDk0MzkwNzEyODk3IiwiaXNzIjoiaHR0cHM6Ly9hcGkuemVlay5uZXR3b3JrIiwic2Fhc0lkIjoiemVlayIsImV4cCI6MTczNjkyNzY1OSwiaWF0IjoxNzM2MzIyODU5LCJqdGkiOm51bGx9.2TlxQ9WmuQkWxw5YP7eQXC8-OvTVMh-xRLvsPsaQp2I23h49Zeh0vfxrL-CtZcHRfwz5uaHihQNQZgR512qRwA',
            'saas_id': 'zeek',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Accept': '*/*',
            'Host': 'api.deek.network',
            'Connection': 'keep-alive'
        }

        # 发送 GET 请求
        response = requests.get(url, headers=headers, params=params)

        # 打印响应内容
        print(response.status_code)  # 打印 HTTP 状态码
        print(response.text)  # 打印响应内容
        return response.text
    except Exception as e:
        print(f"获取推文时出错: {e}")
        return json.dumps(["hello every ony,are you ok?", "how are you", "hahahhahaha", "wow it is nice" , "i like this"])
tools = [add, multiply, getTweet, getDeekTweet]

