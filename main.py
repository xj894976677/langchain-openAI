from llm_handler import *
from models import Joke
from examples import prompt, examples

if __name__ == "__main__":
    # teach_ai("Tell me a joke about planes", examples, prompt, Joke)
    # get_answer("你是谁？")
    # get_struct_answer("Tell me a joke about planes", Joke)
    #
    answer_by_tool("What is 3 * 12? Also, what is 11 + 49?")


