import json
import logging
import os
import re
import subprocess
import time
from typing import List

import openai
from evaluator import Evaluator, Sample
from template import *
from tool_manager import ToolManager
from tqdm import tqdm

openai.api_key = "YOUR OPENAI API KEY"

PYTHON_INTERPRETER_PATH = "path/to/your/python/environment"


def remove_docstrings(code):
    pattern = r"'''[\s\S]*?'''"
    cleaned_code = re.sub(pattern, "", code)
    return cleaned_code


def extract_api_paths(code: str):
    pattern = r"""call_api\s*\(\s*api_name\s*=\s*(?:f"([^"]+)"|"([^"]+)")"""
    matches = re.findall(pattern, code)
    paths = [m[0] or m[1] for m in matches]
    return paths


def parse_python_outputs(text):
    return re.search(r"```python(.*?)```", text, re.DOTALL).group(1).strip()


def construct_input_message(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    return messages


def single_run(messages, retry=3, model="gpt-4o-mini", temperature=0.0):
    for _ in range(retry):
        try:
            output = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                n=1,
                temperature=temperature,
            )
            return output.choices[0].message.content.strip()
        except:
            time.sleep(10)
    return None


def run_planner(chat_history: List[dict], api_descriptions: str) -> str:
    return parse_python_outputs(
        single_run(
            construct_input_message(
                PLANNER_PROMPT.format(
                    dialogue_history=chat_history, toolbox=api_descriptions
                )
            )
        )
    )


def run_cot_planner(chat_history: List[dict], api_descriptions: str) -> str:
    step1_code = single_run(
        construct_input_message(
            PLANNER_COT_STEP_1_PROMPT.format(dialogue_history=chat_history)
        )
    )
    step2_code = single_run(
        messages=construct_input_message(
            prompt=PLANNER_COT_STEP_2_PROMPT.format(
                dialogue_history=chat_history,
                python_function=step1_code,
                toolbox=api_descriptions,
            )
        )
    )
    return parse_python_outputs(step1_code), parse_python_outputs(step2_code)


def run_main_code(main_code: str, retry=3):
    exec_result = subprocess.run(
        [PYTHON_INTERPRETER_PATH, "-c", main_code],
        capture_output=True,
        text=True,
    )
    output = exec_result.stdout
    error = exec_result.stderr
    return output, error


def evaluate(tool_manager: ToolManager, sample: Sample, api_name: str, result: dict):
    ground_truth = sample.ground_truth
    if api_name != ground_truth["api_name"]:
        return False, "API Name Mismatch: {} vs {}".format(
            api_name, ground_truth["api_name"]
        )
    api = tool_manager.init_tool(api_name)
    try:
        correct = api.check_api_call_correctness(result, ground_truth["result"])
    except KeyError:
        correct = False
        result = "KeyError" + str(result)
    return correct, result


def construct_tool_manager_calls(chat_history: list) -> str:
    api_calls = ""
    for chat in chat_history:
        if chat["role"] == "API":
            key_value_str = []
            for k in chat["param_dict"]:
                if chat["param_dict"][k].startswith("[") or chat["param_dict"][
                    k
                ].startswith("{"):
                    key_value_str.append(f"{k}={chat['param_dict'][k]}")
                else:
                    key_value_str.append(f"{k}='{chat['param_dict'][k]}'")
            api_calls += f"""tool_manager.api_call(tool_name='{chat["api_name"]}', {', '.join(key_value_str)})\n"""
    return api_calls


def convert_api_call_to_code_as_action(api_name, param_dict):
    text = "{}(".format(api_name)
    for k, v in param_dict.items():
        text += "{}='{}', ".format(k, v)
    text = text[:-2] + ")"
    return "[" + text + "]"


def expand_chat_history(chat_history):
    messages = []
    for item in chat_history:
        if item["role"] == "API":
            api_call_str = convert_api_call_to_code_as_action(
                item["api_name"], item["param_dict"]
            )
            messages.append(
                {
                    "role": "AI",
                    "text": "I need to call the API: {}".format(api_call_str),
                }
            )
            messages.append(
                {
                    "role": "User",
                    "text": f"The response from the API: {item['result']['output']}. Please go on.",
                }
            )
        else:
            messages.append(item)
    return messages


def revise_code(chat_history: list, main_code: str, error: str):
    for _ in range(3):
        main_code = parse_python_outputs(
            single_run(
                construct_input_message(
                    EXECUTION_FAILURE_TEMPLATE.format(
                        dialogue_history=chat_history,
                        python_code=main_code,
                        execution_result=error,
                    )
                )
            )
        )
        output, error = run_main_code(main_code)
        if not error:
            break
    return main_code, output, error


def main():
    data_dir = "lv1-lv2-samples/level-1-given-desc"
    if os.path.basename(data_dir).endswith("given-desc"):
        tool_search_enabled = False
    else:
        tool_search_enabled = True
    jsonl_files = [f for f in os.listdir(data_dir) if f.endswith(".jsonl")]

    correct = 0
    total = 0

    output_dir = f"results/{data_dir.split('/')[-1]}/"
    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, "eval.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    logging.info("Data dir: {}".format(data_dir))
    logging.info("Output dir: {}".format(output_dir))

    tool_manager = ToolManager()

    result_list = []

    for file in tqdm(jsonl_files, desc="Processing files", ncols=100):
        logging.info("File Name: {}".format(file))
        history = []
        with open(os.path.join(data_dir, file), "r") as f:
            for line in f:
                history.append(json.loads(line))
        samples = Sample.from_chat_history(history)
        evaluator = Evaluator(samples)

        for sample_id in evaluator.get_all_sample_ids():

            sample = evaluator.dataset[sample_id]

            if sample.ground_truth["role"] == "API":

                total += 1
                if tool_search_enabled:
                    _, chat_history = evaluator.get_model_input(sample_id)
                    api_descriptions = evaluator.get_api_description("ToolSearcher")
                    for chat in chat_history:
                        if chat["role"] == "API" and chat["api_name"] == "ToolSearcher":
                            api_descriptions = "\n".join(
                                [json.dumps(out) for out in chat["result"]["output"]]
                            )
                else:
                    api_descriptions, chat_history = evaluator.get_model_input(
                        sample_id
                    )

                chat_history = expand_chat_history(chat_history)

                try:
                    planner_code = run_planner(
                        chat_history=chat_history, api_descriptions=api_descriptions
                    )

                    if len(extract_api_paths(remove_docstrings(planner_code))) > 1:
                        planner_code = single_run(
                            construct_input_message(
                                REPLAN_TEMPLATE.format(
                                    dialogue_history=chat_history,
                                    toolbox=api_descriptions,
                                    initial_code=planner_code,
                                )
                            )
                        )

                    pred_api_name = extract_api_paths(planner_code)[-1]

                    logging.info("Predict API: {}".format(pred_api_name))
                    logging.info(
                        "Ground Truth API Name: {}".format(
                            sample.ground_truth["api_name"]
                        )
                    )

                    main_code = (
                        API_CALL_CODE.format(
                            api_calls=construct_tool_manager_calls(chat_history)
                        )
                        + planner_code
                    )
                    exec_output, exec_error = run_main_code(main_code=main_code)

                    if exec_error:
                        main_code, exec_output, exec_error = revise_code(
                            chat_history=chat_history,
                            main_code=main_code,
                            error=exec_error,
                        )

                    with open(os.path.join(output_dir, f"{total}.py"), "w") as f:
                        f.write(main_code)

                    logging.info("Predict Result: {}".format(exec_output.strip()))
                    logging.info("Predict Error: {}".format(exec_error))
                    logging.info(
                        "Ground Truth Result: {}".format(sample.ground_truth["result"])
                    )

                    if exec_output:
                        is_correct, model_output_result = evaluate(
                            tool_manager,
                            sample,
                            api_name=pred_api_name,
                            result=eval(exec_output.strip()),
                        )
                        logging.info("Eval Result: {}".format(is_correct))
                        correct += 1 if is_correct else 0
                    else:
                        is_correct = False

                    result_list.append(
                        {
                            "file": file,
                            "sample_id": sample_id,
                            "total_id": total,
                            "chat_history": chat_history,
                            "api_descriptions": api_descriptions,
                            "code": main_code,
                            "pred_api_name": pred_api_name,
                            "output": exec_output,
                            "error": exec_error,
                            "ground_truth": sample.ground_truth["result"],
                            "eval_result": is_correct,
                        }
                    )
                except:
                    pass

    logging.info("Accuracy: {:.4f}".format(correct / total))

    with open(os.path.join(output_dir, "exec_result.json"), "w") as f:
        json.dump(result_list, f, indent=4)


if __name__ == "__main__":
    main()
