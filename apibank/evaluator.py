import logging
import re
import time

import openai
from api_call_extraction import APIParseError, parse_api_call
from rouge import Rouge
from termcolor import colored
from tool_manager import ToolManager

openai.api_key = "YOUR OPENAI API KEY"

BASE_CALL_PROMPT = """Based on the given API description and the existing conversation history 1..t, please generate the API request that the AI should call in step t+1 and output it in the format of {format_guide}, replace the ApiName with the actual API name, and replace the key and value with the actual parameters.
Your output should start with a square bracket "[" and end with a square bracket "]". Do not output any other explanation or prompt or the result of the API call in your output. 
This year is 2023.
Input: 
User: [User's utterence]
AI: [AI's utterence]

Expected output:
{expected_output}

API descriptions:
"""

BASE_RESPONSE_PROMPT = """Based on the given API description and the existing conversation history 1..t, please generate the next dialog that the AI should response after the API call t.
This year is 2023.
Input: 
User: [User's utterence]
AI: [AI's utterence]
{expected_output}

Expected output:
AI: [AI's utterence]

API descriptions:
"""


def single_run(messages, retry=3, model_name="gpt-4o-mini", temperature=0.0):
    for _ in range(retry):
        try:
            output = openai.ChatCompletion.create(
                model=model_name,
                messages=messages,
                n=1,
                temperature=temperature,
            )
            return output
        except:
            time.sleep(10)
    return None


def calculate_rouge_l_score(reference, hypothesis):
    rouge = Rouge()
    scores = rouge.get_scores(hypothesis, reference)
    rouge_l_score = scores[0]["rouge-l"]["f"]
    return rouge_l_score


class Sample:
    def __init__(self, chat_history, apis, ground_truth):
        self.chat_history = chat_history
        self.apis = apis
        self.ground_truth = ground_truth

    def __repr__(self):
        return "Sample(chat_history={}, apis={}, ground_truth={})".format(
            self.chat_history, self.apis, self.ground_truth
        )
        # return 'Chat history: {}, apis: {}, ground truth: {}'.format(self.chat_history, self.apis, self.ground_truth)

    @classmethod
    def from_chat_history(cls, chat_history):
        apis = set()
        api_positions = []
        for i, item in enumerate(chat_history):
            if item["role"] == "API":
                apis.add(item["api_name"])
                api_positions.append(i)

        samples = []
        for i in api_positions:
            sample = cls(chat_history[:i], apis, chat_history[i])
            samples.append(sample)
            sample = cls(chat_history[: i + 1], apis, chat_history[i + 1])
            samples.append(sample)

        return samples


class Evaluator:

    def __init__(self, samples):
        self.dataset = samples
        self.sample_ids = list(range(len(self.dataset)))

    def get_all_sample_ids(self):
        return self.sample_ids

    def get_api_description(self, api_name):
        tool_manager = ToolManager()
        return tool_manager.get_api_description(api_name)

    def get_model_input(self, sample_id):
        sample = self.dataset[sample_id]
        apis = sample.apis
        chat_history = sample.chat_history
        tool_manager = ToolManager()
        api_descriptions = []
        for api_name in apis:
            api_descriptions.append(tool_manager.get_api_description(api_name))
        api_descriptions = "\n".join(api_descriptions)
        return api_descriptions, chat_history

    def evaluate(self, sample_id, model_output, action_mode):
        assert action_mode in ["text_as_action", "json_as_action", "code_as_action"]
        # model_output: text_as_action [Action: ApiName, param1: value1, param2: value2, ...]
        # model_output: json_as_action [{"action": "ApiName", "param1": "value1", "param2": "value2", ...}]
        # model_output: code_as_action [ApiName(param1=value1, param2=value2), ...)]
        tool_manager = ToolManager()

        sample = self.dataset[sample_id]
        ground_truth = sample.ground_truth
        if ground_truth["role"] == "API":
            logging.info(f"** Model output: {colored(model_output, 'yellow')}")
            try:
                api_name, param_dict = parse_api_call(model_output, action_mode)
            except APIParseError as e:
                return False, str(e)
            logging.info(
                f"** Parsed API call: {colored(api_name, 'green')}, {colored(param_dict, 'green')}"
            )
            if api_name != ground_truth["api_name"]:
                return False, "API Name Mismatch: {} vs {}".format(
                    api_name, ground_truth["api_name"]
                )
            try:
                result = tool_manager.api_call(api_name, **param_dict)
            except Exception as e:
                return False, str(e)
            api = tool_manager.init_tool(api_name)
            try:
                correct = api.check_api_call_correctness(result, ground_truth["result"])
            except KeyError:
                correct = False
                result = "KeyError" + str(result)
            return correct, result
        elif ground_truth["role"] == "AI":
            score = calculate_rouge_l_score(ground_truth["text"], model_output)
            return round(score, 4)


def get_api_call(model_output):
    # api_call_pattern = r"\[(\w+)\((.*)\)\]"
    api_call_pattern = r"\[(.*)\]"
    api_call_pattern = re.compile(api_call_pattern)
    match = api_call_pattern.search(model_output)
    if match:
        return match.group(0)
    else:
        return None


ACTION_MODE_TO_CALL_PROMPT = {
    "code_as_action": BASE_CALL_PROMPT.format(
        format_guide="[ApiName(key1='value1', key2='value2', ...)]",
        expected_output="[ApiName(key1='value1', key2='value2', ...)]",
    ),
    "text_as_action": BASE_CALL_PROMPT.format(
        format_guide="[Action: ApiName, key1: value1, key2: value2, ...]",
        expected_output="[Action: ApiName, key1: value1, key2: value2, ...]",
    ),
    "json_as_action": BASE_CALL_PROMPT.format(
        format_guide='[{"action": "ApiName", "param1": "value1", "param2": "value2", ...}]',
        expected_output='[{"action": "ApiName", "param1": "value1", "param2": "value2", ...}]',
    ),
}


ACTION_MODE_TO_RESPONSE_PROMPT = {
    "code_as_action": BASE_RESPONSE_PROMPT.format(
        expected_output="[ApiName(key1='value1', key2='value2', ...)]"
    ),
    "text_as_action": BASE_RESPONSE_PROMPT.format(
        expected_output="[Action: ApiName, key1: value1, key2: value2, ...]"
    ),
    "json_as_action": BASE_RESPONSE_PROMPT.format(
        expected_output='[{"action": "ApiName", "param1": "value1", "param2": "value2", ...}]'
    ),
}


def combine_assistant_messages(messages):
    # if there's to consecutive assistant messages, combine them
    combined_messages = []
    for message in messages:
        if (
            message["role"] == "assistant"
            and combined_messages
            and combined_messages[-1]["role"] == "assistant"
        ):
            combined_messages[-1]["content"] += "\n" + message["content"]
        else:
            combined_messages.append(message)
    return combined_messages
