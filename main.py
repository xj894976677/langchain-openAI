from chat_bot import chat, async_chat
from llm_handler import *
from models import Joke
from examples import prompt, examples
import asyncio

if __name__ == "__main__":
    # teach_ai("Tell me a joke about planes", examples, prompt, Joke)
    # get_answer("你是谁？")
    # get_struct_answer("Tell me a joke about planes", Joke)
    #
    # answer_by_tool("What is 3 * 12?")
    # asyncio.get_event_loop().run_until_complete(query_stream("what color is the sky?"))
    # asyncio.get_event_loop().run_until_complete(parser_stream("parrot"))
    # asyncio.get_event_loop().run_until_complete(get_country(
    #     "output a list of the countries france, spain and japan and their populations in JSON format. "
    #     'Use a dict with an outer key of "countries" which contains a list of countries. '
    #     "Each country should have the key `name` and `population`"
    # ))
    # tongyi_get_answer("你是谁？")
    # debug_llm()
    chat()
    # asyncio.get_event_loop().run_until_complete(async_chat(""))
    # trimmer()