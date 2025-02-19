from typing import Optional, Type
from datetime import datetime
from pydantic import BaseModel, Field

class TwitterTweet(BaseModel):
    """推文的数据模型"""
    content: str = Field(description="推文内容")
    created_at: datetime = Field(description="发布时间")
    author: str = Field(description="作者")

class TwitterAPI:
    """模拟的 Twitter API 实现"""
    def __init__(self):
        # 模拟的推文数据库
        self._tweets = {
            "elonmusk": [
                TwitterTweet(
                    content="Just had a great meeting about Starship progress!",
                    created_at=datetime(2025, 2, 17, 10, 30),
                    author="elonmusk"
                )
            ],
            "OpenAI": [
                TwitterTweet(
                    content="Announcing GPT-5: A new milestone in AI development",
                    created_at=datetime(2025, 2, 17, 9, 0),
                    author="OpenAI"
                )
            ]
        }
    
    def get_latest_tweet(self, username: str) -> Optional[TwitterTweet]:
        """获取指定用户的最新推文"""
        if username.startswith("@"):
            username = username[1:]
        
        user_tweets = self._tweets.get(username, [])
        return user_tweets[0] if user_tweets else None
