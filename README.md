# langchain-openAI

## Install
```bash
pip install --upgrade pip
pip install -qU langchain-openai
pip install --upgrade --quiet langchain-community dashscope
# 持久层实现，可以持续聊天
pip install -U langgraph

pip install transformers

# 代理功能所需的全部包
pip install -U langchain-community langgraph langchain-anthropic tavily-python langgraph-checkpoint-sqlite
pip install tweepy

1. https://tavily.com/ 访问这个网站获取 Tavilys Search API 并且添加到环境变量中 TAVILY_API_KEY


```

## Usage
本项目基于ali qwen模型，使用LangChain框架 https://python.langchain.com/docs/how_to/streaming/ 实现其中部分用例以及扩展