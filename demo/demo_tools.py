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
def getDeekTweets(username: str) -> str:
    """
        获取指定用户在deek平台的最新100条推文。按照发布时间倒序排列
        :param username: 用户名
        :return: 以json的形式返回当前用户的100条推文内容
        """
    try:
        url = 'https://api.deek.network/v1/feed/wish/timeline'
        params = {
            'nextToken': '',
            'limit': 10,
            'customerId': username,
            'role': 'MAKER'
        }
        # 请求头
        headers = {
            'jwt_token': 'eyJraWQiOiI4dnVrYmYxbmxtdGo1ZGE2d3owcTJyeGk5c2hjcHkzNyIsInR5cCI6IkpXVCIsImFsZyI6IkVTMjU2In0.eyJzdWIiOiJ0YWxlbnQiLCJhdWQiOiIyMDI0MDkyMzA4NDk0MzkwNzEyODk3IiwidWlkIjoiMjAyNDA5MjMwODQ5NDM5MDcxMjg5NyIsIndzS2V5IjoiU2N5Y2RlOFgiLCJuYmYiOjE3Mzk1MzMyNDgsInVzZXJfaWQiOiIyMDI0MDkyMzA4NDk0MzkwNzEyODk3IiwiY2hhaW5JZCI6ODAwODQsImlzcyI6Imh0dHBzOi8vYXBpLnplZWsubmV0d29yayIsInNhYXNJZCI6InplZWsiLCJleHAiOjE3NDAxMzgwNDgsImlhdCI6MTczOTUzMzI0OCwianRpIjpudWxsfQ.nCG9CdTzPcEymL9-msKV8PmCgodaccuDyUu1zLx_icE5EnAumZzcV9-2diNwXS4emEFpNU53n9kDOUG92SdcbQ',
            'chain_id': '80084',
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
        json_object = json.loads(response.text)
        print(json_object['obj']['rows'])
        return json_object['obj']['rows']
    except Exception as e:
        print(f"获取推文时出错: {e}")
        return json.dumps(["hello every ony,are you ok?", "how are you", "hahahhahaha", "wow it is nice" , "i like this"])


@tool
def getDeekFollowers(username: str) -> str:
    """
        获取指定用户在deek平台上的关注用户信息
        :param username: 用户名
        :return: 以数组的形式返回关注用户的id
        """
    try:
        import requests

        # 请求 URL 和参数
        url = 'https://api.opensocial.fun/v2/relations/profiles/0x488a/followers'
        params = {
            'with_reverse': 'true',
            'with_profile': 'true',
            'limit': 20,
            'ranking': 'CREATED'
        }

        # 请求头
        headers = {
            'sec-ch-ua-platform': '"macOS"',
            'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiIweDkxMGM5YjIzYjIzMjcyMWRiNmIzNDAzMzE1YTI5OTk4OTc4MTRlYTIiLCJhdWQiOiI5NDgxMTI2ODgzNzI3ODIyOCIsIm5iZiI6MTczOTUzMzI0NywiY2hhaW5zIjpbeyJvc3BBZGRyZXNzIjoiMHgwODNiMjg1YjZkMGUwZTg3MTFjMGQ2NzNlNTgwMmRhMzVmNGYxNmUxIiwiY2hhaW5JZCI6IjgwMDg0IiwicGVybWlzc2lvbnMiOltdLCJwcm9maWxlSWQiOiIweDQ4OGEiLCJzdGF0dXMiOiJBQ1RJVkUifV0sIm9zcE93bmVySWQiOiIyMDI0MDkyMzA4NDk0NDY3MzkzMjYzIiwiYXBwSWQiOiI5NDgxMTI2ODgzNzI3ODIyOCIsImlzcyI6Imh0dHBzOi8vb3BlbnNvY2lhbC5mdW4iLCJlb2FBZGRyZXNzIjoiMHg5MTBjOWIyM2IyMzI3MjFkYjZiMzQwMzMxNWEyOTk5ODk3ODE0ZWEyIiwiZXhwIjoxNzM5NTY5MjQ3LCJpYXQiOjE3Mzk1MzMyNDd9.q3wNDtV7j6HXyHLTd4e2GGA7eVF8v22d0KqlNVNahBFMyKJAaeWLqgTpvWhokLADIlU9C9I0ljpZXJ-Ed6lD6A',
            'Referer': 'https://m.deek.network/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'OS-Guest-Id-Marketing': '3141597425322673',
            'OS-App-Id': '94811268837278228',
            'OS-Chain-Id': '80084',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'a': '[object Object]'
        }

        # 发送 GET 请求
        response = requests.get(url, headers=headers, params=params)
        # 打印响应内容
        print(response.status_code)  # 打印 HTTP 状态码
        print(response.text)  # 打印响应内容
        json_object = json.loads(response.text)
        print(json_object['data']['rows'])
        print([item['handle'] for item in json_object['data']['rows']])
        return getDeekFollowersByCustomerId([item['handle'] for item in json_object['data']['rows']])
    except Exception as e:
        print(f"获取关注用户时出错: {e}")
        return


def getDeekTweetContent(tweetId: str) -> str:
    import requests

    # 设置请求头
    headers = {
        'sec-ch-ua-platform': '"macOS"',
        'Referer': 'https://m.deek.network/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'jwt_token': 'eyJraWQiOiI4dnVrYmYxbmxtdGo1ZGE2d3owcTJyeGk5c2hjcHkzNyIsInR5cCI6IkpXVCIsImFsZyI6IkVTMjU2In0.eyJzdWIiOiJ0YWxlbnQiLCJhdWQiOiIyMDI0MDkyMzA4NDk0MzkwNzEyODk3IiwidWlkIjoiMjAyNDA5MjMwODQ5NDM5MDcxMjg5NyIsIndzS2V5IjoiU2N5Y2RlOFgiLCJuYmYiOjE3Mzk1MzMyNDgsInVzZXJfaWQiOiIyMDI0MDkyMzA4NDk0MzkwNzEyODk3IiwiY2hhaW5JZCI6ODAwODQsImlzcyI6Imh0dHBzOi8vYXBpLnplZWsubmV0d29yayIsInNhYXNJZCI6InplZWsiLCJleHAiOjE3NDAxMzgwNDgsImlhdCI6MTczOTUzMzI0OCwianRpIjpudWxsfQ.nCG9CdTzPcEymL9-msKV8PmCgodaccuDyUu1zLx_icE5EnAumZzcV9-2diNwXS4emEFpNU53n9kDOUG92SdcbQ',
        'chain_id': '80084',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'saas_id': 'zeek'
    }

    # 设置URL和查询参数
    url = 'https://api.deek.network/v1/quest/list'
    params = {
        'bizIds': tweetId
    }

    # 发送GET请求
    response = requests.get(url, headers=headers, params=params)

    # 输出返回的JSON内容
    print(response.json())


def getDeekFollowersByCustomerId(customerIds) -> []:
    # 请求 URL
    url = 'https://api.deek.network/v1/profile'

    # 请求头
    headers = {
        'sec-ch-ua-platform': '"macOS"',
        'Referer': 'https://m.deek.network/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'jwt_token': 'eyJraWQiOiI4dnVrYmYxbmxtdGo1ZGE2d3owcTJyeGk5c2hjcHkzNyIsInR5cCI6IkpXVCIsImFsZyI6IkVTMjU2In0.eyJzdWIiOiJ0YWxlbnQiLCJhdWQiOiIyMDI0MDkyMzA4NDk0MzkwNzEyODk3IiwidWlkIjoiMjAyNDA5MjMwODQ5NDM5MDcxMjg5NyIsIndzS2V5IjoiU2N5Y2RlOFgiLCJuYmYiOjE3Mzk1MzMyNDgsInVzZXJfaWQiOiIyMDI0MDkyMzA4NDk0MzkwNzEyODk3IiwiY2hhaW5JZCI6ODAwODQsImlzcyI6Imh0dHBzOi8vYXBpLnplZWsubmV0d29yayIsInNhYXNJZCI6InplZWsiLCJleHAiOjE3NDAxMzgwNDgsImlhdCI6MTczOTUzMzI0OCwianRpIjpudWxsfQ.nCG9CdTzPcEymL9-msKV8PmCgodaccuDyUu1zLx_icE5EnAumZzcV9-2diNwXS4emEFpNU53n9kDOUG92SdcbQ',
        'chain_id': '80084',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'saas_id': 'zeek',
        'Content-Type': 'application/json'
    }

    # 请求体数据
    data = {
        "idList": customerIds,
        "badgeStrategy": "HNWI",
        "needBadgeInfo": True,
        "needOpenSocialInfo": False
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 打印响应内容
    print(response.status_code)  # 打印 HTTP 状态码
    print(response.json())  # 打印响应的 JSON 数据
    print([item['basic']['customerId'] for item in response.json()['obj']['rows']])
    return [item['basic']['customerId'] for item in response.json()['obj']['rows']]
tools = [add, multiply, getTweet, getDeekTweets, getDeekFollowers]

