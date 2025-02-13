import ast
import json
import re
import subprocess
import time
from difflib import SequenceMatcher
from typing import List

import openai
from tmdb_template import *
from tqdm import tqdm

openai.api_key = "YOUR OPENAI API KEY"

PYTHON_INTERPRETER_PATH = "path/to/your/python/environment"
TMDB_API_KEY = "PUT/YOUR/API/KEY/HERE"


def calculate_similarity(path1, path2):
    segments1 = path1.strip("/").split("/")
    segments2 = path2.strip("/").split("/")

    max_length = max(len(segments1), len(segments2))
    segments1 += [""] * (max_length - len(segments1))
    segments2 += [""] * (max_length - len(segments2))

    score = 0
    for s1, s2 in zip(segments1, segments2):
        if "{" in s1 or "{" in s2:
            score += 1
        elif s1 == s2:
            score += 2
        else:
            score += SequenceMatcher(None, s1, s2).ratio()
    return score / (2 * max_length)


def find_most_similar_api(input_api, api_collection, top_n=3):
    similarities = [
        (api, calculate_similarity(input_api, api)) for api in api_collection
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [api for api, _ in similarities[:top_n]]


def remove_docstrings(code):
    pattern = r"'''[\s\S]*?'''"
    cleaned_code = re.sub(pattern, "", code)
    return cleaned_code


def extract_api_paths(code: str):
    pattern = r"""call_api\s*\(\s*api_path\s*=\s*(?:f"([^"]+)"|"([^"]+)")"""
    matches = re.findall(pattern, code)
    paths = [m[0] or m[1] for m in matches]
    return paths


def parse_planner_outputs(text):
    return json.loads(re.search(r"```json(.*?)```", text, re.DOTALL).group(1).strip())


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


def chain_of_thought_planner(query, tmdb_toolbox, code_function):
    code_comment_function = parse_python_outputs(
        single_run(
            messages=construct_input_message(
                prompt=PLANNER_TEMPLATE_STEP.format(
                    question=query, toolbox=tmdb_toolbox, pseudo_code_task=code_function
                )
            ),
            temperature=0.0,
        )
    )
    cot_output = single_run(
        messages=construct_input_message(
            prompt=FUNCTION_TEMPLATE.format(
                question=query,
                toolbox=tmdb_toolbox,
                pseudo_code_task=f"```python\n{code_comment_function}\n```",
            )
        ),
        temperature=0.0,
    )
    return cot_output


def revise_plan(
    query: str,
    code_solution: str,
    called_apis: List[str],
    toolpaths: List[str],
    toolbox_dict: List[dict],
) -> List[dict]:
    for _ in range(3):
        missing_apis = []
        for api in called_apis:
            if api not in toolpaths:
                missing_apis.append(api)
        if len(missing_apis) > 0:
            similar_toolpaths = []
            for api in missing_apis:
                similar_toolpaths.extend(find_most_similar_api(api, toolpaths))
            similar_toolpaths = list(set(similar_toolpaths))
            similar_toolbox = [
                {
                    "path": api,
                    "functionality": toolbox_dict[api]["functionality"],
                }
                for api in similar_toolpaths
            ]
            code_solution = parse_python_outputs(
                single_run(
                    construct_input_message(
                        REPLAN_TEMPLATE.format(
                            question=query,
                            pseudo_code_solution=code_solution,
                            missing_apis=missing_apis,
                            toolbox=similar_toolbox,
                        )
                    )
                )
            )
            called_apis = extract_api_paths(code_solution)
        else:
            break
    return code_solution


def run_assembler(
    question: str,
    code_solution: str,
    tmdb_oas_dict: dict,
) -> str:
    called_apis = extract_api_paths(remove_docstrings(code_solution))
    similar_apis = [
        find_most_similar_api(api, tmdb_oas_dict.keys(), top_n=1)[0]
        for api in called_apis
    ]
    api_doc = [
        {
            "path": tmdb_oas_dict[api]["path"],
            "parameters": tmdb_oas_dict[api]["parameters"],
            "schema": tmdb_oas_dict[api]["schema"],
        }
        for api in similar_apis
    ]
    main_code = single_run(
        construct_input_message(
            prompt=REUSABLE_ASSEMBLY_MAIN_FUNCTION_TEMPLATE.format(
                question=question,
                code_solution=code_solution,
                api_doc=api_doc,
                api_key=TMDB_API_KEY,
            )
        )
    )
    return parse_python_outputs(main_code)


def run_main_code(main_code: str, retry=3):
    output = None
    error = None
    for _ in range(retry):
        exec_result = subprocess.run(
            [PYTHON_INTERPRETER_PATH, "-c", main_code],
            capture_output=True,
            text=True,
        )
        output = exec_result.stdout
        error = exec_result.stderr
        if not exec_result.stderr:
            break
    return output, error


def extract_functions_from_code(code_string):
    tree = ast.parse(code_string)
    function_definitions = [
        node for node in tree.body if isinstance(node, ast.FunctionDef)
    ]
    functions = []
    for func in function_definitions:
        start_line = func.lineno - 1
        end_line = func.end_lineno
        func_code = "\n".join(code_string.splitlines()[start_line:end_line])
        functions.append(func_code)
    return functions


def revise_code(question: str, main_code: str, error: str):
    for _ in range(3):
        main_code = parse_python_outputs(
            single_run(
                construct_input_message(
                    EXECUTION_FAILURE_TEMPLATE.format(
                        question=question,
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
    with open("datasets/tmdb_oas.json", "r") as f:
        tmdb_oas_data = json.load(f)

    toolbox = [
        {
            "path": item["path"],
            "functionality": item["functionality"],
        }
        for item in tmdb_oas_data
    ]
    toolpaths = [api["path"] for api in toolbox]
    toolbox_dict = {item["path"]: item for item in tmdb_oas_data}

    with open("datasets/tmdb_v3.json", "r") as f:
        test_data = json.load(f)
    print(len(test_data))

    for test_item in tqdm(test_data):
        try:
            code_function = parse_python_outputs(
                single_run(
                    construct_input_message(
                        CODE_FUNCTION_PROMPT.format(question=test_item["query"])
                    )
                )
            )
            test_item["code_function"] = code_function

            code_solution = chain_of_thought_planner(
                query=test_item["query"],
                tmdb_toolbox=toolbox,
                code_function=test_item["code_function"],
            )
            test_item["code_solution"] = parse_python_outputs(code_solution)
            called_apis = extract_api_paths(parse_python_outputs(code_solution))
            test_item["called_apis"] = called_apis

            code_solution = revise_plan(
                query=test_item["query"],
                code_solution=code_solution,
                called_apis=called_apis,
                toolpaths=toolpaths,
                toolbox_dict=toolbox_dict,
            )
            called_apis = extract_api_paths(code_solution)
            test_item["code_solution"] = code_solution
            test_item["called_apis"] = called_apis

            main_code = run_assembler(
                question=test_item["query"],
                code_solution=code_solution,
                tmdb_oas_dict=toolbox_dict,
            )
            test_item["main_code"] = main_code

            output, error = run_main_code(main_code=main_code)
            test_item["output"] = output
            test_item["error"] = error

            if error:
                revised_code, output, error = revise_code(
                    test_item["query"], test_item["main_code"], test_item["error"]
                )
                test_item["main_code"], test_item["output"], test_item["error"] = (
                    revised_code,
                    output,
                    error,
                )

            print("Query: ", test_item["query"])
            print("Solution: ", test_item["solution"])
            print("Genrated Paths: ", called_apis)
            print("=" * 100)
        except:
            continue

    with open("results/toolcoder_tmdb.json", "w") as f:
        json.dump(test_data, f, indent=4)


if __name__ == "__main__":
    main()
