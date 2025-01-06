from agent.agent import getTwitter, getAdd
from chat_bot import chat
import asyncio

from common.llm_handler import answer_by_tool

if __name__ == "__main__":
    # teach_ai("Tell me a joke about planes", examples, prompt, Joke)
    # get_answer("你是谁？")
    # get_struct_answer("Tell me a joke about planes", Joke)
    #
    answer_by_tool("elonmusk 最新的一条帖文是什么内容")
    # asyncio.get_event_loop().run_until_complete(query_stream("what color is the sky?"))
    # asyncio.get_event_loop().run_until_complete(parser_stream("parrot"))
    # asyncio.get_event_loop().run_until_complete(get_country(
    #     "output a list of the countries france, spain and japan and their populations in JSON format. "
    #     'Use a dict with an outer key of "countries" which contains a list of countries. '
    #     "Each country should have the key `name` and `population`"
    # ))
    # tongyi_get_answer("你是谁？")
    # debug_llm()
    # chat()
    # asyncio.get_event_loop().run_until_complete(async_chat(""))
    # trimmer()
    # 测试推文
    # asyncio.get_event_loop().run_until_complete(getTwitter())
    # asyncio.get_event_loop().run_until_complete(getAdd())

