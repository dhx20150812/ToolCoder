import ast
import json
import re
import subprocess
import time
from typing import List

import openai
from spotify_template import *
from tqdm import tqdm

openai.api_key = "YOUR OPENAI API KEY"

PYTHON_INTERPRETER_PATH = "path/to/your/python/environment"

RAW_SPOTIFY_INITIALIZATION_TEMPLATE = """
import os
import yaml
import json
from langchain_community.utilities import Requests
from spotify_utils import *
import spotipy

config = yaml.load(open("./config.yaml", "r"), Loader=yaml.FullLoader)
os.environ["SPOTIPY_CLIENT_ID"] = config["spotipy_client_id"]
os.environ["SPOTIPY_CLIENT_SECRET"] = config["spotipy_client_secret"]
os.environ["SPOTIPY_REDIRECT_URI"] = config["spotipy_redirect_uri"]

with open("./datasets/spotify_oas.json") as f:
    raw_api_spec = json.load(f)

scopes = list(
    raw_api_spec["components"]["securitySchemes"]["oauth_2_0"]["flows"][
        "authorizationCode"
    ]["scopes"].keys()
)
access_token = spotipy.util.prompt_for_user_token(scope=",".join(scopes))
headers = {"Authorization": f"Bearer {access_token}"}
requests_wrapper = Requests(headers=headers)
init_spotify(requests_wrapper=requests_wrapper)

"""


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


def parse_python_outputs(text):
    return re.search(r"```python(.*?)```", text, re.DOTALL).group(1).strip()


def extract_request_url_pairs(input_text):
    pattern = r"\b(GET|POST|PUT|DELETE)\s(/[\w/{}/-]+)"
    matches = re.findall(pattern, input_text)
    return matches


def is_solution_subsequence(solution, task_decompose_result):
    solution_index = 0
    for path in task_decompose_result:
        if solution_index < len(solution) and solution[solution_index] == path:
            solution_index += 1
        if solution_index == len(solution):
            return True
    return False


def remove_docstrings(code):
    pattern = r"'''[\s\S]*?'''"
    cleaned_code = re.sub(pattern, "", code)
    return cleaned_code


def gen_api_description_str(spotify_oas_data):
    api_list = []
    for tool in spotify_oas_data:
        for method in ["get", "post", "delete", "put"]:
            if tool.get(method):
                api_list.append(
                    {
                        "path": tool["path"],
                        "method": method,
                        "description": tool[method]["detailed_description"],
                    }
                )

    tool_desc = ""
    for i, tool in enumerate(api_list):
        tool_desc += f"- {tool['method'].upper()} https://api.spotify.com/v1{tool['path']}: {tool['description']}\n"
    return tool_desc


def run_planner(query, spotify_oas_data, code_function):
    tool_desc = gen_api_description_str(spotify_oas_data=spotify_oas_data)

    code_comment_function = parse_python_outputs(
        single_run(
            messages=construct_input_message(
                prompt=PLANNER_TEMPLATE_STEP.format(
                    question=query,
                    toolbox=tool_desc,
                    pseudo_code_task=code_function,
                )
            ),
        )
    )
    return code_comment_function


def gen_main_code(query, code_comment_function, spotify_oas_data):
    spotify_toolbox_dict = {tool["path"]: tool for tool in spotify_oas_data}
    code_impl_toolbox = [
        {
            "path": path,
            "method": method.lower(),
            "description": spotify_toolbox_dict[path][method.lower()][
                "detailed_description"
            ],
            # + " "
            # + spotify_toolbox_dict[path][method.lower()]["guideline"],
            "parameters": spotify_toolbox_dict[path][method.lower()].get(
                "parameters", []
            ),
            "schema": spotify_toolbox_dict[path][method.lower()]["schema"],
            "requestBody": spotify_toolbox_dict[path][method.lower()].get(
                "requestBody", {}
            ),
            "implementation_example": spotify_toolbox_dict[path][method.lower()].get(
                "implementation_example", ""
            ),
        }
        for method, path in extract_request_url_pairs(code_comment_function)
    ]
    print(len(code_impl_toolbox))
    main_code = parse_python_outputs(
        single_run(
            messages=construct_input_message(
                prompt=REUSABLE_FUNCTION_TEMPLATE.format(
                    # prompt=FUNCTION_TEMPLATE.format(
                    question=query,
                    toolbox=json.dumps(code_impl_toolbox),
                    pseudo_code_task=code_comment_function,
                )
            ),
        )
    )
    return main_code


def run_main_code(main_code: str, retry=3):
    exec_result = subprocess.run(
        [PYTHON_INTERPRETER_PATH, "-c", main_code],
        capture_output=True,
        text=True,
    )
    output = exec_result.stdout
    error = exec_result.stderr
    return output, error


def run_replan(query: str, code_comment_function: str, spotify_oas_data: List[dict]):
    spotify_oas_paths = [item["path"] for item in spotify_oas_data]
    tool_desc = gen_api_description_str(spotify_oas_data=spotify_oas_data)
    pattern = r"(?i)Call\s+(\w+)\s+(/[\w/{}/-]+)"
    match = re.findall(pattern, remove_docstrings(code_comment_function))

    if len(match):
        feedbacks = "No planning content described by comments was detected in the code. Please ensure that the planning results are provided in the form of comments instead of implementing specific functions."
        revised_code_comment_function = parse_python_outputs(
            single_run(
                messages=construct_input_message(
                    prompt=REPLAN_TEMPLATE.format(
                        toolbox=tool_desc,
                        question=query,
                        pseudo_code_solution=code_comment_function,
                        feedback=feedbacks,
                    )
                )
            )
        )
        return revised_code_comment_function

    invalid_urls = []
    for method, url in match:
        if url not in spotify_oas_paths:
            invalid_urls.append(url)
    if len(invalid_urls) != 0:
        feedbacks = "\n".join(
            [
                f"The `{url}` API is invalid as it is not existed in the provided toolbox. Please check it and replace it with an appropriate one. "
                for url in invalid_urls
            ]
        )
        revised_code_comment_function = parse_python_outputs(
            single_run(
                messages=construct_input_message(
                    prompt=REPLAN_TEMPLATE.format(
                        toolbox=tool_desc,
                        question=query,
                        pseudo_code_solution=code_comment_function,
                        feedback=feedbacks,
                    )
                )
            )
        )
        return revised_code_comment_function

    return code_comment_function


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


def extract_first_function_body_as_strings(code):
    # Parse the code into an Abstract Syntax Tree (AST)
    tree = ast.parse(code)
    statements = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for stmt in node.body:
                start_lineno = stmt.lineno - 1
                end_lineno = getattr(stmt, "end_lineno", stmt.lineno)
                statement_lines = code.splitlines()[start_lineno:end_lineno]
                statement = "\n".join(statement_lines).strip()
                statements.append(statement)
            break

    return statements


def extract_http_methods_and_urls(code):
    pattern = re.compile(
        r'requests_wrapper\.(get|post|put|delete)\(\s*[f]?["\'](https?://[^\s"\']+)'
    )
    matches = pattern.findall(code)
    return matches


def collect_successful_api_calls(main_code, reusable_toolbox):
    for line in extract_first_function_body_as_strings(main_code):
        methods_and_urls = extract_http_methods_and_urls(line)
        for method, url in methods_and_urls:
            url = url.replace("https://api.spotify.com/v1", "")
            reusable_toolbox[url][method]["implementation_example"] = line.strip()
    return reusable_toolbox


def main():
    with open("./datasets/spotify_oas_toolcoder.json", "r") as f:
        spotify_oas_data = json.load(f)

    with open("./datasets/spofity.json", "r") as f:
        spofity_test_data = json.load(f)
    print(len(spofity_test_data))

    with_refelction = True
    reusable_toolbox = spotify_oas_data

    for test_item in tqdm(spofity_test_data):
        try:
            code_function = parse_python_outputs(
                single_run(
                    construct_input_message(
                        CODE_FUNCTION_PROMPT.format(question=test_item["query"])
                    )
                )
            )
            test_item["code_function"] = code_function

            code_comment_function = run_planner(
                query=test_item["query"],
                spotify_oas_data=spotify_oas_data,
                code_function=code_function,
            )
            test_item["planner_solution"] = code_comment_function

            if with_refelction:
                code_comment_function = run_replan(
                    query=test_item["query"],
                    code_comment_function=code_comment_function,
                    spotify_oas_data=spotify_oas_data,
                )
                test_item["planner_solution"] = code_comment_function

            code_solution = gen_main_code(
                query=test_item["query"],
                code_comment_function=code_comment_function,
                spotify_oas_data=reusable_toolbox,
            )
            test_item["code_solution"] = code_solution

            main_code = RAW_SPOTIFY_INITIALIZATION_TEMPLATE + code_solution
            test_item["main_code"] = main_code

            output, error = run_main_code(main_code=main_code)
            test_item["output"] = output
            test_item["error"] = error

            if error and with_refelction:
                revised_code, output, error = revise_code(
                    test_item["query"], test_item["main_code"], test_item["error"]
                )
                test_item["main_code"], test_item["output"], test_item["error"] = (
                    revised_code,
                    output,
                    error,
                )

            if not error and "Failed" not in test_item["output"]:
                reusable_toolbox = collect_successful_api_calls(
                    main_code=test_item["main_code"], reusable_toolbox=reusable_toolbox
                )

            print("Query: ", test_item["query"])
            print("Solution: ", test_item["solution"])
            print(
                "Generated Paths: ",
                [
                    method + " " + path
                    for method, path in extract_request_url_pairs(code_comment_function)
                ],
            )
            print("=" * 100)
        except:
            pass

    with open(
        "./results/toolcoder_spotify.json",
        "w",
    ) as f:
        json.dump(spofity_test_data, f, indent=4)


if __name__ == "__main__":
    main()
