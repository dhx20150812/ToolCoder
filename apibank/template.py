PLANNER_COT_STEP_1_PROMPT = """You are a planning assistant tasked with deciding the immediate next action in a tool learning task. Your role is to analyze the dialogue history and determine what action the system should take next, focusing only on the next step and not the overall goal. Use Python code to create a function that captures this decision.

## Instructions:
1. **Analyze the dialogue history**:
    - Identify the next immediate action required.
    - Use the conversation history to infer the most logical next step.
    - Do not attempt to resolve the entire task; focus only on the immediate action.
2. **Function Name**:
    - Name the function based on the next action identified.
    - Choose a concise, meaningful function name that accurately reflects the task's purpose.
3. **Docstring**:
    - A brief description that explains the purpose of the function and the identified next step.
    - Represent the relevant dialogue history as comments in the function to provide context.
    - Use triple single quotes (`'''`) for the docstring, as shown below.
4. **Function Body**:
    - Leave the function body empty. Only include the function definition, parameters, and docstring in your output.
5. **Example Execution Block**:
   - Add an `if __name__ == "__main__":` block that demonstrates how to call the function with realistic arguments.
   - Do not include placeholders; use only specific data available from the dialogue history.
   - For fields that are not explicit names, times, or other specific values (such as reminders, symptoms, meeting or schedule content), use highly summarized phrases to describe the content.
   - Ensure that time-related parameters are formatted as `%Y-%m-%d %H:%M:%S` unless otherwise specified.
   - This block should serve as a guide for users on how to execute the function in a standalone script.
6. **Temporal Consistency**:
    - Assume the current year is 2023. All dates or time-related values involving a year must use 2023 unless explicitly stated otherwise in the dialogue.

Here are some examples:
### Example 1:
#### Dialogue History
{{"role": "User", "text": "Can you help me find out about shortness of breath?"}}
{{"role": "AI", "text": "Sure, I can call the EmergencyKnowledge API to search for information about shortness of breath."}}
### Output Python Function
```python
def search_information_for_symptom(symptom: str):
    '''
    Search for information about a specific symptom.

    Notes:
    - This function does not contain logic for execution; it only identifies the action to be taken next.
    - Next step identified: Use the EmergencyKnowledge API to retrieve information about the specific symptom.

    Dialogue Context:
    # User: Can you help me find out about shortness of breath?
    # AI: Sure, I can call the EmergencyKnowledge API to search for information about shortness of breath.
    '''
    # Function logic goes here

if __name__ == "__main__":
    information = search_information_for_symptom(symptom="shortness of breath")
    print("Information about shortness of breath: ", information)
```

### Example 2:
#### Dialogue History
{{"role": "User", "text": "Can you help me register an appointment with a specific doctor on a specific date?"}}
{{"role": "AI", "text": "Sure, I can help you with that. Please provide me with the patient's name, doctor's name and the date of the appointment."}}
{{"role": "User", "text": "The patient's name is John Smith, the doctor's name is Dr. Johnson, and the date is June 1st, 2022."}}
{{"role": "AI", "text": "Okay, I will register an appointment for John Smith with Dr. Johnson on June 1st, 2022. Just a moment please."}}
### Output Python Function
```python
def register_appointment(patient_name: str, doctor_name: str, date: str):
    '''
    Register an appointment with a specific doctor on a specific date.

    Note
    - This function does not contain logic for execution; it only identifies the action to be taken next.
    - Next step identified: register an appointment for John Smith with Dr. Johnson on June 1st, 2022.

    Dialogue History
    # User: Can you help me register an appointment with a specific doctor on a specific date?
    # AI: Sure. Please provide me with the patient's name, doctor's name and the date of the appointment.
    # User: The patient's name is John Smith, the doctor's name is Dr. Johnson, and the date is June 1st, 2022.
    # AI: Okay, I will register an appointment for John Smith with Dr. Johnson on June 1st, 2022.
    '''
    # Function logic goes here

if __name__ == "__main__":
    register_appointment(
        patient_name="John Smith", date="2022-06-01", doctor_name="Dr. Johnson"
    )
```

### Example 3
#### Dialogue History
{{'role': 'User', 'text': 'Can you add a reminder for a meeting on 2022-05-06 at 2 PM?'}}
{{'role': 'AI', 'text': 'Sure, I can do that. For which username should I add the reminder?'}}
{{'role': 'User', 'text': 'user1'}}
{{'role': 'AI', 'text': 'I also need your password to authenticate. Can you please tell me your username and password?'}}
{{'role': 'User', 'text': 'user1 user1pass'}}
{{'role': 'AI', 'text': "Call API: [GetUserToken(username='user1', password='user1pass')]"}}
{{'role': 'User', 'text': "You have got a response: {{'token': 'n9m8k7j6h5g4f3d2s1a0'}}"}}
### Output Python Function
```python
def add_reminder(token: str, content: str, time: str):
    '''
    Add a reminder for a meeting.

    Note
    - This function does not contain logic for execution; it only identifies the action to be taken next.
    - Next step identified: The AI have authenticated the account and got a token. So the next step for the AI is to add a reminder for a meeting on 2022-05-06 at 2 PM.

    Dialogue History
    # User: Can you add a reminder for a meeting on 2022-05-06 at 2 PM?
    # AI: Sure, I can do that. I need to authenticate your account. Can you please tell me your username and password?
    # User: user1 user1pass
    # AI: Okay. I will call the API `GetUserToken(username='user1', password='user1pass')` to authenticate your account.
    # User: After call the API, you got a response: {{'token': 'n9m8k7j6h5g4f3d2s1a0'}}
    '''
    # Function logic goes here

if __name__ == "__main__":
    add_reminder(
        token="n9m8k7j6h5g4f3d2s1a0", content="Meeting", time="2022-05-06 14:00:00"
    )
```

Now, it's your turn!
### Dialogue History
{dialogue_history}
### Output Python Function
"""

PLANNER_COT_STEP_2_PROMPT = """You are a coding assistant tasked with implementing the internal logic of a function identified in the first step of the tool learning process. Using the function structure and the provided toolbox, select an appropriate API and fill in the function’s body.

## Instructions:
1. **Use the provided function structure**:
   - Complete the function body based on the purpose and next step defined in its docstring.
   - Use only one API call from the provided toolbox that fulfills the function’s purpose.
2. **API Selection**:
   - Choose the API that best matches the required next step.
   - Extract the necessary parameters for the API from the conversation history.
   - Modify parameter names in this function to match the API's parameter names if necessary.
   - For fields that are not explicit names, times, or other specific values (such as reminders, symptoms, meeting or schedule content), use highly summarized phrases to describe the content.
   - Ensure that time-related parameters are formatted as `%Y-%m-%d %H:%M:%S` unless otherwise specified.
3. **Function Body**:
   - Implement the API call using the format `call_api(api_name="example", params={{...}})`.
   - Do not include placeholders; use only specific data available from the dialogue history.
   - Print the result of the API call using a statement like `print(results)`.
   - You should print the OVERALL result, not a specific field. For instance, we prefer `print(balance_results)` rather than `print(balance_results['balance'])`.
4. **Example Execution Block**:
   - Adjust the `if __name__ == "__main__":` block to match the API's parameter names if necessary.
   - Do not include placeholders; use only specific data available from the dialogue history.
   - This block should serve as a guide for users on how to execute the function in a standalone script.

### Example 1:
#### Dialogue History
{{"role": "User", "text": "Can you help me find out about shortness of breath?"}}
{{"role": "AI", "text": "Sure, I can call the EmergencyKnowledge API to search for information about shortness of breath."}}
#### Python Function
```python
def search_information_for_symptom(symptom: str):
    '''
    Search for information about a specific symptom.

    Notes:
    - This function does not contain logic for execution; it only identifies the action to be taken next.
    - Next step identified: Use the EmergencyKnowledge API to retrieve information about the specific symptom.

    Dialogue Context:
    # User: Can you help me find out about shortness of breath?
    # AI: Sure, I can call the EmergencyKnowledge API to search for information about shortness of breath.
    '''
    # Function logic goes here

if __name__ == "__main__":
    information = search_information_for_symptom(symptom="shortness of breath")
    print("Information about shortness of breath: ", information)
```
#### API Toolbox
{{"name": "ModifyRegistration", "description": "This API modifies the registration of a patient given appointment ID.", "input_parameters": {{"appointment_id": {{"type": "str", "description": "The ID of appointment."}}, "new_appointment_date": {{"type": "str", "description": "The new appointment date. Format: %Y-%m-%d."}}, "new_appointment_doctor": {{"type": "str", "description": "The new appointment doctor."}}}}, "output_parameters": {{"status": {{"type": "str", "description": "The status of modification."}}}}}}
{{"name": "EmergencyKnowledge", "description": "This API searches for a given symptom for emergency knowledge.", "input_parameters": {{"symptom": {{"type": "str", "description": "The symptom to search."}}}}, "output_parameters": {{"results": {{"type": "list", "description": "The list of results. Format be like [{{\"name\":possible disease name, \"aid\": first-aid method}},...]"}}}}}}
{{"name": "RecordHealthData", "description": "This API records the health data of a user.", "input_parameters": {{"user_id": {{"type": "str", "description": "The ID of user."}}, "time": {{"type": "str", "description": "The time of health data. Format: %Y-%m-%d %H:%M:%S"}}, "health_data": {{"type": "list", "description": "The health data, with the format like [{{'name': 'blood_pressure', 'value': '120/80'}}, {{'name': 'heart_rate', 'value': '80'}}]"}}}}, "output_parameters": {{"status": {{"type": "str", "description": "The status of recording."}}}}}}
#### Output Python Solution
```python
def search_information_for_symptom(symptom: str):
    '''
    Search for information about a specific symptom.

    Notes:
    - This function does not contain logic for execution; it only identifies the action to be taken next.
    - Next step identified: Use the EmergencyKnowledge API to retrieve information about the specific symptom.

    Dialogue Context:
    # User: Can you help me find out about shortness of breath?
    # AI: Sure, I can call the EmergencyKnowledge API to search for information about shortness of breath.
    '''
    results = call_api(api_name="EmergencyKnowledge", params={{"symptom": "shortness of breath"}})
    print(results)

if __name__ == "__main__":
    information = search_information_for_symptom(symptom="shortness of breath")
    print("Information about shortness of breath: ", information)
```

Now, it's your turn!
#### Dialogue History
{dialogue_history}
#### Python Function
{python_function}
#### API Toolbox
{toolbox}
#### Output Python Solution
"""

PLANNER_PROMPT = """You are an advanced coding assistant designed to model human-AI collaboration for tool learning. Your task is to generate a Python function that reflects the user's goal and selects the most appropriate API from a provided toolbox to achieve that goal. The function must be designed to predict only the next step, and therefore, it should call exactly one API using `call_api`.

## Instructions:

1. **Analyze the Next Step**:
   - Begin by analyzing the dialogue history to determine the immediate next step required to advance toward the user's goal.
   - Focus on executing only the next actionable task rather than solving the user's overall objective.
   - Identify which API from the toolbox can fulfill this immediate need.
2. **Function Name**: Derive a concise and descriptive function name based on the identified next step.
3. **Parameters**: Identify essential inputs for the API call directly from the dialogue and define them with appropriate type annotations. 
   - Use only information explicitly present in the dialogue. Do not invent placeholders or use ambiguous values.
4. **Return Type**: Omit the return statement; the function must print the API's result instead of returning it.
5. **Docstring**: Write a detailed docstring that includes:
   - A brief description of the function’s purpose, specifically the immediate next step being executed.
   - A description of each parameter, including its type and purpose.
   - Note that the function will print the result instead of returning it.
   - **API Usage Constraints**:
       - The function must call exactly one API using `call_api`.
       - Each `call_api` invocation must use a fixed `api_name` from the toolbox; do not modify or invent paths.
       - Place all request parameters within a `params` dictionary.
       - Example usage: `call_api(api_name="example", params={{"key": value}})`.
6. **Dialogue History**: Represent relevant parts of the dialogue history as comments within the function to provide context.
7. **Temporal Consistency**: Assume the current year is 2023. All dates or time-related values involving a year must use 2023 unless explicitly stated otherwise in the dialogue.
8. **Function Body**:
   - Implement only the necessary logic to invoke the selected API with `call_api`.
   - Print the result of the API call using a statement like `print(results)`.
   - Do not include additional operations or API calls. The function must directly use input data derived from the dialogue, and avoid placeholders for any missing or unclear information.
9. **Example Usage**:
   - At the end of your code, include an `if __name__ == "__main__":` block demonstrating how to call the function with realistic arguments derived from the dialogue context.
   - This block should serve as a guide for users on how to execute the function in a standalone script.

## Example:
### Conversation History
{{"role": "User", "text": "Can you help me find out about shortness of breath?"}}
{{"role": "AI", "text": "Sure, I can call the EmergencyKnowledge API to search for information about shortness of breath."}}
### Toolbox
{{"name": "RecordHealthData", "description": "This API records the health data of a user.", "input_parameters": {{"user_id": {{"type": "str", "description": "The ID of user."}}, "time": {{"type": "str", "description": "The time of health data. Format: %Y-%m-%d %H:%M:%S"}}, "health_data": {{"type": "list", "description": "The health data, with the format like [{{'name': 'blood_pressure', 'value': '120/80'}}, {{'name': 'heart_rate', 'value': '80'}}]"}}}}, "output_parameters": {{"status": {{"type": "str", "description": "The status of recording."}}}}}}
{{"name": "ModifyRegistration", "description": "This API modifies the registration of a patient given appointment ID.", "input_parameters": {{"appointment_id": {{"type": "str", "description": "The ID of appointment."}}, "new_appointment_date": {{"type": "str", "description": "The new appointment date. Format: %Y-%m-%d."}}, "new_appointment_doctor": {{"type": "str", "description": "The new appointment doctor."}}}}, "output_parameters": {{"status": {{"type": "str", "description": "The status of modification."}}}}}}
{{"name": "EmergencyKnowledge", "description": "This API searches for a given symptom for emergency knowledge.", "input_parameters": {{"symptom": {{"type": "str", "description": "The symptom to search."}}}}, "output_parameters": {{"results": {{"type": "list", "description": "The list of results. Format be like [{{\"name\":possible disease name, \"aid\": first-aid method}},...]"}}}}}}
### Output Python Function:
```python
def search_emergency_knowledge_for_symptom(symptom: str) -> list:
    '''
    Searches for emergency knowledge related to a specific symptom.

    Parameters:
    symptom (str): The symptom to search for emergency knowledge.

    Returns:
    list: A list of results with possible disease names and first-aid methods. 
          Each result is formatted as {{"name": <disease name>, "aid": <first-aid method>}}.

    Notes:
    - This function uses the EmergencyKnowledge API.
    - API usage example:
      call_api(api_name="EmergencyKnowledge", params={{"symptom": symptom}})
    - Ensure the provided symptom is accurately described for meaningful results.

    Dialogue Context:
    # User: Can you help me find out about shortness of breath?
    # AI: Sure, I can call the EmergencyKnowledge API to search for information about shortness of breath.
    '''

    # API call
    results = call_api(api_path="EmergencyKnowledge", params={{"symptom": symptom}})
    print(results)

if __name__ == "__main__":
    search_emergency_knowledge_for_symptom(symptom="shortness of breath")
```

Now, it's your turn!
### Conversation History
{dialogue_history}
### Toolbox
{toolbox}
### Output Python Function (with only one API call):
"""

API_CALL_CODE = """
from tool_manager import ToolManager

tool_manager = ToolManager()
{api_calls}
def call_api(api_name, params):
    result = tool_manager.api_call(api_name, **params)
    return result

"""

REPLAN_TEMPLATE = """Your task is to modify a provided Python code snippet to focus on implementing the next step of the task by making a single API call, based on the conversation history and API description provided. 

## Input:
You will receive the following information:
1. **Conversation History**: A log of the ongoing interaction with the user.
2. **API Description**: A detailed description of the available API, including its parameters, expected input, and output format.
3. **Initial Python Code**: A Python code snippet that may contain multiple API calls or logic unrelated to the next immediate step.

## Output:
Generate a revised Python code snippet that adheres to the following rules:
1. **Single API Call**: Ensure the modified code snippet includes exactly one API call (`call_api`). Remove any additional API calls or logic not relevant to the next step. 
2. **Focus on the Next Step**: The modified code should address only the next immediate step based on the input context (conversation history and API description). Do not attempt to fulfill the user's overall goal within a single snippet.
3. **Function Output**: The function or code snippet should print the result of the API call using a statement like `print(results)`.
4. **Preserve the function's return format**: The function should return the OVERALL result, not a specific field. For instance, we prefer `print(balance_results)` istead of `print(balance_results['balance'])`.
5. **Preserve Relevance**: Retain any context or variables from the initial code necessary for the next API call but avoid introducing unrelated changes.

## Instructions:
1. Review the conversation history to understand the user's intent and the next step in the task.
2. Examine the API description to construct the correct API call for the next step.
3. Analyze the provided initial Python code:
   - Identify and retain relevant parts of the code that are required for the next API call.
   - Remove extraneous API calls or logic unrelated to the next step.
4. Generate a modified Python code snippet that aligns with the requirements in the "Output" section above.


## Example
### Initial Python Code
```
def get_user_token_and_modify_alarm(username: str, password: str, alarm_time: str) -> None:
    '''
    Retrieves the user token and modifies the alarm to a specified time.

    Parameters:
    username (str): The username of the user.
    password (str): The password of the user.
    alarm_time (str): The new alarm time in the format '%Y-%m-%d %H:%M:%S'.

    Notes:
    - This function first retrieves the user token using the GetUserToken API,
      then modifies the alarm using the ModifyAlarm API with the provided time.
    - The current date for the alarm change is assumed to be 2023-03-16, the day after today's date.

    Dialogue Context:
    # User: Can you modify my alarm for tomorrow morning at 7am? Today is 2023-03-15.
    # AI: Sure, I can help you with that. What's your username?
    # User: JohnDoe
    # AI: Thanks, can you provide me with your password?
    # User: pass123
    # AI: Got it. Now let me authenticate you.
    '''

    # Step 1: Get the user token
    token_response = call_api(api_name="GetUserToken", params={{"username": username, "password": password}})
    token = token_response['output']['token']

    # Step 2: Modify the alarm to 2023-03-16 07:00:00
    modify_response = call_api(api_name="ModifyAlarm", params={{"token": token, "from_time": "2023-03-15 07:00:00", "to_time": "2023-03-16 07:00:00"}})
    print(modify_response)

if __name__ == "__main__":
    get_user_token_and_modify_alarm(username="JohnDoe", password="pass123", alarm_time="2023-03-16 07:00:00")
```
### Revised Python Code
```python
def get_user_token(username: str, password: str) -> None:
    '''
    Retrieves the user token.

    Parameters:
    username (str): The username of the user.
    password (str): The password of the user.

    Notes:
    - This function retrieves the user token using the GetUserToken API,

    Dialogue Context:
    # User: Can you modify my alarm for tomorrow morning at 7am? Today is 2023-03-15.
    # AI: Sure, I can help you with that. What's your username?
    # User: JohnDoe
    # AI: Thanks, can you provide me with your password?
    # User: pass123
    # AI: Got it. Now let me authenticate you.
    '''

    # Get the user token
    token_response = call_api(api_name="GetUserToken", params={{"username": username, "password": password}})
    print(token_response)

if __name__ == "__main__":
    get_user_token(username="JohnDoe", password="pass123")
```
According to the conversation history, the next step should be to authenticate the user's identity, so the modified code only uses API GetUserToken, simplifying the functions and processes of the initial code.

Now it's your turn!
### Conversation History
{dialogue_history}
### API Descriptions
{toolbox}
Initial Python Code
```python
{initial_code}
```
Revised Code (only one API calls):
"""

EXECUTION_FAILURE_TEMPLATE = """You were asked to answer the user's question by writing python code to call appreciate APIs and print the final answer. However, the code execution failed for some reasons. Your task is to analyze the error message and revise the code accordingly. Follow these detailed guidelines:

### Instructions:
1. **Analyze the error stack**: Review the provided error message to locate the source of the issue. Identify the specific line where the error occurs.
2. **Modify only the error-causing line**: Focus solely on correcting the line that triggered the error. Avoid making changes to other parts of the code.
3. **Preserve the function's return format**: The function should return the OVERALL result, not a specific field. For instance:
```python
balance_results = call_api(api_name="QueryBalance", params={{"token": token}})
print(balance_results)
```
Avoid modifying the code to return or print specific fields, such as:
```python
print(balance_results['output']['balance'])
```
or
```python
print(balance_results['balance'])
```

#### Special Case for KeyError:
For example, if a `KeyError` like this occurs:
  ```python
  token = token_response["token"]
  ```
  You can correct this code to navigate to the correct key as follows:
  ```python
  token = token_response["output"]["token"]
  ```
But remember to print the overall result of the final result instead of a specific field.

Now, it's your turn!
### Conversation History
{dialogue_history}

The Python code you previously generated is:  
```python
{python_code}
```
However, the code execution failed with the following result:
============
{execution_result}
============

Using the dialogue history, the provided code, and the error message as references, generate revised Python code that resolves the issue and successfully accomplishes the user's goal.

Return the revised Python code below:
"""
