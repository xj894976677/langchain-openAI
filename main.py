from llm_handler import get_struct_answer, get_answer, teach_ai
from models import Joke
from examples import prompt, examples

if __name__ == "__main__":
    teach_ai("Tell me a joke about planes", examples, prompt, Joke)
    get_answer("你是谁？")

    get_struct_answer("Tell me a joke about planes", Joke)


