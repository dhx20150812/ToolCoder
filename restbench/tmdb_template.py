PLANNER_TEMPLATE_STEP = """Your objective is to analyze the user's complex question and create a breakdown of actionable subtasks, identifying the most appropriate APIs from the provided toolbox to address each subtask in sequence.

### Available Tools:
{toolbox}

Each API includes a request path and a description of its functionality. Utilize these APIs strategically to decompose and solve the user's question according to the following guidelines:

#### Guidelines
1. **Clarify Requirements**: Carefully read the user's question to determine key requirements, objectives, and expected outcomes. Identify any specific data or information you need to gather to satisfy the request.
2. **Break Down the Task**: Divide the complex task into clear, manageable subtasks that each address part of the user's needs and can be fulfilled using one or more APIs.
3. **Select Relevant APIs**: Match each subtask to the most relevant API(s) from the toolbox. Base your choices on each API's functionality and response format to ensure it provides the required information.
4. **Handle Dependencies**: Check for dependencies between APIs. For example, to access `/3/movie/{{movie_id}}/credits`, the `movie_id` must first be retrieved via a compatible API.
5. **Output in Pseudo-Code**: Write your solution as a Python function using pseudo-code, with each step annotated in comments (denote as Step 1 to N) describing the subtask. **Do not write any code implementation for the steps—only document the subtasks in comments.**

### Example:
Question: give me the number of movies directed by Sofia Coppola
Pseudo-Code Task:
```python
def get_directed_movie_count(director_name: str) -> int:
    '''
    Get the number of movies directed by a specific director.

    Parameters:
        director_name (str): The full name of the director whose movies to count.

    Returns:
        int: The number of movies directed by the specified director.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - All request parameters should be placed in the `params` dictionary.
    '''
    # Function logic goes here

if __name__ == "__main__":
    number_of_movies_directed = get_directed_movie_count(director_name="Sofia Coppola")
    print("Number of movies directed by Sofia Coppola:", number_of_movies_directed)
```

Planned Subtasks:
```python
def get_directed_movie_count(director_name: str) -> int:
    '''
    Get the number of movies directed by a specific director.

    Parameters:
        director_name (str): The full name of the director whose movies to count.

    Returns:
        int: The number of movies directed by the specified director.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - All request parameters should be placed in the `params` dictionary.
    '''

    # Step 1. Search for Sofia Coppola using the /3/search/person API to find her person_id.

    # Step 2. Retrieve the movie credits for Sofia Coppola using her person_id with the /3/person/{{person_id}}/movie_credits API.

    # Step 3. Count the number of movies in the credits retrieved.

if __name__ == "__main__":
    number_of_movies_directed = get_directed_movie_count(director_name="Sofia Coppola")
    print("Number of movies directed by Sofia Coppola:", number_of_movies_directed)
```

**User's Question**: {question}
**Pseudo-Code Task**:
```python
{pseudo_code_task}
```
Planned Subtasks:
"""

FUNCTION_TEMPLATE = """You task is to help the user select appropriate APIs from the provided toolbox and complete the function template to solve the problem accurately.

## Instructions

1. **Input Provided**:
   - **Problem Description**: A specific question or request from the user (e.g., "give me the number of movies directed by Sofia Coppola").
   - **Pseudo-Code Task Template**: A function template with the following components:
     - Function signature, parameters, return type, and a functional description.
     - Structured subtask comments directly embedded in the pseudo-code template, outlining each planned subtask step-by-step.

2. **Expected Output**:
   - Based on the problem description and the structured action plan provided, complete the pseudo-code by selecting and integrating suitable API calls from the provided candidate toolbox.
   - Use the placeholder `call_api(api_path, params)` for each API call, where:
     - `api_path` strictly matches a valid, existing API path from the provided candidate toolbox. Do not create or assume any non-existent API paths. **No `api_path` outside this toolbox should be used or inferred.**
     - Place all request parameters within the `params` dictionary; do not format `api_path` using string interpolation or formatted strings.
     - Example: use `call_api(api_path="/3/movie/{{movie_id}}/credits", params={{"movie_id": movie_id}})` instead of `call_api(api_path=f"/3/movie/{{movie_id}}/credits", params={{}})`.

3. **Guidelines for API Selection**:
   - Do not provide a direct answer to the problem. Instead, fill in the pseudo-code template to enable successful execution.
   - Follow these steps for each `call_api` integration:
     - Identify any necessary preliminary calls (e.g., fetching an entity ID).
     - Ensure each step logically contributes to the function’s purpose, using helper variables and conditional checks where needed.
     - Keep pseudo-code succinct, adding comments that clarify the role of each API call.

## Example Scenarios:
**Example 1:**
Question: give me the number of movies directed by Sofia Coppola
Pseudo-Code Task:
```python
def get_directed_movie_count(director_name: str) -> int:
    '''
    Get the number of movies directed by a specific director.

    Parameters:
        director_name (str): The full name of the director whose movies to count.

    Returns:
        int: The number of movies directed by the specified director.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - All request parameters should be placed in the `params` dictionary.
    '''
    # Step 1: Search for the director using /3/search/person API to find person_id.
    # Step 2: Retrieve movie credits for the director using their person_id with the /3/person/{{person_id}}/movie_credits API.
    # Step 3: Filter the credits to include only movies directed by this director and count them.

if __name__ == "__main__":
    number_of_movies_directed = get_directed_movie_count(director_name="Sofia Coppola")
    print("Number of movies directed by Sofia Coppola:", number_of_movies_directed)
```

Pseudo-Code Solution:
```python
def get_directed_movie_count(director_name: str) -> int:
    '''
    Get the number of movies directed by a specific director.

    Parameters:
        director_name (str): The full name of the director whose movies to count.

    Returns:
        int: The number of movies directed by the specified director.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - All request parameters should be placed in the `params` dictionary.
    '''
    # Step 1: Search for the director using /3/search/person API to find person_id.
    person_search_response = call_api(api_path="/3/search/person", params={{"query": "Sofia Coppola"}})
    
    # Get person_id from response
    person_id = person_search_response.get("results")[0]["id"]

    # Step 2: Retrieve movie credits for the director using their person_id with the /3/person/{{person_id}}/movie_credits API.
    movie_credits_response = call_api(api_path="/3/person/{{person_id}}/movie_credits", params={{"person_id": person_id}})

    # Step 3: Filter the credits to include only movies directed by this director and count them.
    directed_movies = [
        movie for movie in movie_credits_response["crew"]
        if movie["job"] == "Director"
    ]

    # Step 5: Get the count of directed movies
    number_of_movies_directed = len(directed_movies)

    return number_of_movies_directed

if __name__ == "__main__":
    number_of_movies_directed = get_directed_movie_count(director_name="Sofia Coppola")
    print("Number of movies directed by Sofia Coppola:", number_of_movies_directed)
```
**Note**: All `api_path` entries in `call_api` must be chosen strictly from the provided candidate tool set.

**Example 2:**
Question: What is the latest movie directed by Christopher Nolan?
Pseudo-Code Task:
```python
def get_latest_movie_by_director(director_name: str) -> dict:
    '''
    Get the latest movie directed by a specific director.

    Parameters:
        director_name (str): The full name of the director whose latest movie to retrieve.

    Returns:
        dict: A dictionary containing details of the latest movie directed by the specified director, 
              including fields such as 'title', 'release_date', and 'id'. 
              If no movie is found, it may return an empty dictionary or None.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - All request parameters should be placed in the `params` dictionary.
    '''
    # Step 1. Search for movies directed by Christopher Nolan to get relevant movie IDs.
    # Step 2. Retrieve the latest movie from the list of movies directed by Christopher Nolan.

if __name__ == "__main__":
    latest_movie = get_latest_movie_by_director(director_name="Christopher Nolan")
    print("Latest movie directed by Christopher Nolan:", latest_movie)
```

Pseudo-Code Solution:
```python
def get_latest_movie_by_director(director_name: str) -> dict:
    '''
    Get the latest movie directed by a specific director.

    Parameters:
        director_name (str): The full name of the director whose latest movie to retrieve.

    Returns:
        dict: A dictionary containing details of the latest movie directed by the specified director, 
              including fields such as 'title', 'release_date', and 'id'. 
              If no movie is found, it may return an empty dictionary or None.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - All request parameters should be placed in the `params` dictionary.
    '''
    # Step 1: Search for movies directed by Christopher Nolan to get relevant movie IDs.
    person_search_response = call_api(api_path="/3/search/person", params={{"query": director_name}})
    
    # Check if any results found
    if not person_search_response.get("results"):
        return {{}}

    # Get person_id from response
    person_id = person_search_response["results"][0]["id"]

    # Step 2. Retrieve the latest movie from the list of movies directed by Christopher Nolan.
    # Retrieve movie credits for Christopher Nolan using person_id
    movie_credits_response = call_api(api_path="/3/person/{{person_id}}/movie_credits", params={{"person_id": person_id}})
    
    # Filter for movies that Christopher Nolan directed
    directed_movies = [
        movie for movie in movie_credits_response["crew"]
        if movie["job"] == "Director"
    ]
    
    # Sort the directed movies by release date in descending order
    directed_movies_sorted = sorted(directed_movies, key=lambda x: x["release_date"], reverse=True)

    # Get the latest movie (the first in the sorted list)
    if directed_movies_sorted:
        latest_movie = directed_movies_sorted[0]
        return {{
            'title': latest_movie['title'],
            'release_date': latest_movie['release_date'],
            'id': latest_movie['id']
        }}

    return {{}}

if __name__ == "__main__":
    latest_movie = get_latest_movie_by_director(director_name="Christopher Nolan")
    print("Latest movie directed by Christopher Nolan:", latest_movie)
```

## Provided API toolbox:
{toolbox}

Let's begin!
Question: {question}
Pseudo-Code Task:
{pseudo_code_task}
Please complete the pseudo-code solution:
"""

CODE_FUNCTION_PROMPT = """You are a coding assistant specialized in converting task requirements into precise Python function definitions. Your role is to define a function that fully meets the task's objectives by specifying a clear function name, parameters, return type, and docstring.

## Instructions:

For each given task, carefully follow these steps to create a well-structured function definition:
1. **Function Name**: Choose a concise, meaningful function name that accurately reflects the task's purpose.
2. **Parameters**: Identify and define the essential input(s) the function requires. For each parameter:
   - Use a descriptive name and include a type annotation.
3. **Return Type**: Specify an appropriate return type (e.g., `int`, `str`, `dict`, `list`) that best represents the function’s output.
4. **Docstring**: Write a detailed, clear docstring that includes:
   - A brief description of the function’s purpose.
   - Descriptions for each parameter, detailing its type and role.
   - Explanation of the return value, with type and a brief on what it represents.
   - Explicit **Notes** on using `call_api`, with the following rules:
       - Each `call_api` invocation must use an `api_path` from the provided toolbox; do not invent or alter paths.
       - Place all request parameters within the `params` dictionary; do not format `api_path` using string interpolation or formatted strings.
       - Example: use `call_api(api_path="/3/movie/{{movie_id}}/credits", params={{"movie_id": movie_id}})` instead of `call_api(api_path=f"/3/movie/{{movie_id}}/credits", params={{}})`.
       - Refer to the example functions below for guidance on structuring this.
   - Use triple single quotes (`'''`) for the docstring, as shown below.
5. **Function Body**: Leave the function body empty. Only include the function definition, parameters, and docstring in your output.

## Examples:

### Example 1
Here are some example:
Question: What is the latest movie directed by Christopher Nolan?
Python Function:
```python
def get_latest_movie_by_director(director_name: str) -> dict:
    '''
    Get the latest movie directed by a specific director.

    Parameters:
        director_name (str): The full name of the director whose latest movie to retrieve.

    Returns:
        dict: A dictionary containing details of the latest movie directed by the specified director, 
              including fields such as 'title', 'release_date', and 'id'. 
              If no movie is found, it may return an empty dictionary or None.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - Place all request parameters within the `params` dictionary; do not format `api_path` using string interpolation or formatted strings.
        - Example: use `call_api(api_path="/3/movie/{{movie_id}}/credits", params={{"movie_id": movie_id}})` instead of `call_api(api_path=f"/3/movie/{{movie_id}}/credits", params={{}})`.
    '''
    # Function logic goes here

if __name__ == "__main__":
    latest_movie = get_latest_movie_by_director(director_name="Christopher Nolan")
    print("Latest movie directed by Christopher Nolan:", latest_movie)
```

### Example 2
Question: give me the number of movies directed by Sofia Coppola
Python Function:
```python
def get_directed_movie_count(director_name: str) -> int:
    '''
    Get the number of movies directed by a specific director.

    Parameters:
        director_name (str): The full name of the director whose movies to count.

    Returns:
        int: The number of movies directed by the specified director.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - Place all request parameters within the `params` dictionary; do not format `api_path` using string interpolation or formatted strings.
        - Example: use `call_api(api_path="/3/movie/{{movie_id}}/credits", params={{"movie_id": movie_id}})` instead of `call_api(api_path=f"/3/movie/{{movie_id}}/credits", params={{}})`.
    '''
    # Function logic goes here

if __name__ == "__main__":
    number_of_movies_directed = get_directed_movie_count(director_name="Sofia Coppola")
    print("Number of movies directed by Sofia Coppola:", number_of_movies_directed)
```

Now, let's begin!
You are given a question: {question}
Python Function:
"""

REPLAN_TEMPLATE = """Your task is to correct the provided pseudo-code solution to ensure that every API call strictly matches the available APIs in the toolbox. This correction is necessary because some API calls in the initial solution are invalid, meaning they do not exist in the API documentation. Based on the inputs, identify suitable replacements from the toolbox and provide a corrected pseudo-code solution that adheres to the following instructions.

### Objective
- Reflect on the question and the initial code solution to determine how to replace non-existent APIs with those in the toolbox while maintaining the solution's core logic.
- Update the pseudo-code function to replace any invalid API calls with the most appropriate ones from the toolbox.
- Ensure the corrected code preserves the intended functionality and logic.

### Input
1. **Question**: A specific question or request from the user.
2. **Initial Code Solution**: The pseudo-code generated in the previous step, which may contain invalid API paths.
3. **Missing APIs**: A list of API paths extracted from the initial solution that are not present in the toolbox.
4. **Available Tools**: A curated list of valid APIs that include paths similar to the missing APIs, along with their descriptions and usage instructions.

### Expected Output
- A revised pseudo-code solution where all `api_path` entries are validated and replaced appropriately using available APIs from the toolbox.
- The function should maintain its logical consistency and correctly address the user's question.
- The corrected function should use the placeholder format `call_api(api_path, params)` for API calls, with each `api_path` aligning strictly with these APIs in toolbox.

### Guidelines for Revising the Code
1. Understand the Missing APIs:
    - Use the provided list of missing APIs extracted from the initial solution to identify the problematic API calls that need replacement.
2. Select Suitable Replacements:
    - For each missing API in the list, review the provided similar API set (from the toolbox) and select the most appropriate replacement.
    - Match the replacement API to the intended functionality described in the initial solution while maintaining consistency with the overall logic.
3. Adjust Parameters:
    - Modify the parameters of the selected replacement API to align with the structure and requirements of the toolbox entry.
    - Ensure all required parameters for the replacement API are included and correctly named.
4. Maintain Logical Consistency:
    - Verify that the corrected pseudo-code preserves the original logical flow and achieves the intended functionality described in the question.
5. Use Placeholder Format:
    - Structure each API call in the revised pseudo-code as `call_api(api_path, params)` to ensure clarity and adherence to the standard format.

### Below is an example
Question: What does the lead actor of the first episode of second season of Black Mirror look like?
### Initial Code Solution:
```python
def get_lead_actor_of_first_episode_second_season(series_name: str) -> dict:
    '''
    Omitted for simplicity
    '''

    # Step 1: Search for the series "Black Mirror" using the /3/search/tv API to find the series ID.
    series_search_response = call_api(api_path="/3/search/tv", params={{"query": series_name}})
    
    # Omitted for simplicity

    # Step 2: Retrieve details about the second season of "Black Mirror" using the series ID with the /3/tv/{{series_id}}/season/2 API.
    season_details_response = call_api(api_path="/3/tv/{{series_id}}/season/2", params={{"series_id": series_id}})

    # Omitted for simplicity

    # Step 4: Retrieve the credits for the first episode using the /3/tv/{{series_id}}/season/2/episode/{{episode_number}}/credits API to find the lead actor.
    episode_credits_response = call_api(api_path="/3/tv/{{series_id}}/season/2/episode/{{episode_number}}/credits", params={{"series_id": series_id, "episode_number": episode_number}})

    # Omitted for simplicity

    # Step 6: Search for the lead actor's images using the /3/person/{{person_id}}/images API, where person_id is the ID of the lead actor.
    actor_id = lead_actor["id"]
    actor_images_response = call_api(api_path="/3/person/{{actor_id}}/images", params={{"actor_id": actor_id}})

    # Omitted for simplicity

    return {{
        'name': lead_actor['name'],
        'character': lead_actor['character'],
        'image_url': actor_image_url,
    }}

if __name__ == "__main__":
    actor_details = get_lead_actor_of_first_episode_second_season(series_name="Black Mirror")
    print("Lead actor details:", actor_details)
```
### Missing APIs:
["/3/tv/{{series_id}}/season/2", "/3/tv/{{series_id}}/season/2/episode/{{episode_number}}/credits", "/3/person/{{actor_id}}/images"]

### Corrected Code Solution:
```python
def get_lead_actor_of_first_episode_second_season(series_name: str) -> dict:
    '''
    Omitted for simplicity
    '''

    # Step 1: Search for the series "Black Mirror" using the /3/search/tv API to find the series ID.
    series_search_response = call_api(api_path="/3/search/tv", params={{"query": series_name}})
    
    # Omitted for simplicity

    # Step 2: Retrieve details about the second season of "Black Mirror" using the series ID with the /3/tv/{{series_id}}/season/{{season_number}} API.
    season_details_response = call_api(api_path="/3/tv/{{series_id}}/season/{{season_number}}", params={{"series_id": series_id, "season_number": 2}})

    # Omitted for simplicity

    # Step 4: Retrieve the credits for the first episode using the /3/tv/{{series_id}}/season/{{season_number}}/episode/{{episode_number}}/credits API to find the lead actor.
    episode_credits_response = call_api(api_path="/3/tv/{{series_id}}/season/{{season_number}}/episode/{{episode_number}}/credits", params={{"series_id": series_id, "season_number": 2, "episode_number": 1}})

    # Omitted for simplicity

    # Step 6: Search for the lead actor's images using the /3/person/{{person_id}}/images API, where person_id is the ID of the lead actor.
    actor_id = lead_actor["id"]
    actor_images_response = call_api(api_path="/3/person/{{person_id}}/images", params={{"person_id": actor_id}})

    # Omitted for simplicity

    return {{
        'name': lead_actor['name'],
        'character': lead_actor['character'],
        'image_url': actor_image_url,
    }}

if __name__ == "__main__":
    actor_details = get_lead_actor_of_first_episode_second_season(series_name="Black Mirror")
    print("Lead actor details:", actor_details)
```

Now it is your turn!
### Question:
{question}
### Initial Code Solution:
```python
{pseudo_code_solution}
```
### Missing APIs:
{missing_apis}
### Toolbox:
{toolbox}
### Corrected Code Solution:
Please provide the revised pseudo-code below, ensuring all api_path entries match valid paths in the toolbox:
"""

ASSEMBLY_MAIN_FUNCTION_TEMPLATE = """You are a coding assistant specializing in Python and API integration. Your task is to translate code snippets with `call_api` placeholders into executable Python code. Each `call_api` placeholder represents an API call that should be implemented as a separate function.

#### Input:
1. A Python code snippet containing one or more `call_api` placeholders.
2. The OpenAPI documentation describing the APIs, including:
   - Endpoints (`path`),
   - Expected input parameters (`parameters`),
   - Response structure (`schema`).

#### Requirements:
1. **Function Creation**: For each API in the OpenAPI specification:
   - Implement a Python function using the `requests` library.
   - Use `https://api.themoviedb.org` as the `base_url`. Construct the full URL by appending the `api_path` to this `base_url`.
   - Use the `GET` method for all requests.
   - Include two parameters in the function signature:
     - `params`: An optional dictionary for query parameters.
     - `headers`: A mandatory dictionary containing the following:
       ```python
       headers = {{
           "Authorization": "{api_key}"
       }}
       ```
   - Ensure the function returns parsed response data in a usable format.
2. **Integration**: Replace each `call_api` placeholder in the original code with calls to the corresponding functions. Ensure the replacement maintains the original logic.
3. **Error Handling**: Add error handling to manage API failures (e.g., HTTP errors). Use `try/except` blocks to log errors or raise exceptions.
4. **Code Quality**:
   - Write clear and descriptive docstrings for each function.
   - Follow Python best practices for readability and maintainability.

#### Output:
The complete, executable Python code with:
   - Defined functions for each API,
   - Updated logic that calls these functions.

#### Additional Notes:
- Validate input parameters where applicable.
- Ensure all requests include the `headers` defined above.
- Clearly document any assumptions made during implementation.

Here are some examples.
# Question: What is the genre of The Mandalorian?
Input Code:
```python
def get_genre_of_show(show_title: str) -> dict:
    '''
    Get the genre of a specific TV show.

    Parameters:
        show_title (str): The title of the TV show for which to retrieve the genre.

    Returns:
        dict: A dictionary containing the genre(s) of the specified TV show. 
              This may include fields such as 'genres', which is a list of genre names. 
              If no genre is found, it may return an empty dictionary or None.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - Place all request parameters within the `params` dictionary; do not format `api_path` using string interpolation or formatted strings.
    '''
    # Step 1. Search for "The Mandalorian" using the /3/search/tv API to find its series_id.
    search_response = call_api(api_path="/3/search/tv", params={{"query": "The Mandalorian"}})
    
    # Check if any results were found
    if not search_response.get("results"):
        return {{}}

    # Get the series_id from the response
    series_id = search_response["results"][0]["id"]

    # Step 2. Retrieve detailed information about the show using the /3/tv/{{series_id}} with the acquired series_id to get the genres.
    show_details_response = call_api(api_path="/3/tv/{{series_id}}", params={{"series_id": series_id}})

    # Extract genres from the show details
    genres = show_details_response.get("genres", [])

    # Create a dictionary to return genre names
    genre_names = [genre["name"] for genre in genres]

    return {{"genres": genre_names}}

if __name__ == "__main__":
    genre_info = get_genre_of_show(show_title="The Mandalorian")
    print("Genre of The Mandalorian:", genre_info)
```

### Output Code:
```python
import requests

headers = {{
   "Authorization": "{api_key}"
}}

def search_tv_shows(query, first_air_date_year=None, include_adult=False, language="en-US", page=1, year=None):
    '''
    Searches for TV shows based on the provided query and optional parameters.

    Parameters:
    - query (str): The search query for the TV shows. This is a required parameter.
    - first_air_date_year (int, optional): Search only the first air date. Valid values are: 1000..9999.
    - include_adult (bool, optional): Whether to include adult content in the search results. Default is False.
    - language (str, optional): The language code for the response. Default is "en-US".
    - page (int, optional): The page number for pagination. Default is 1.
    - year (int, optional): Search the first air date and all episode air dates. Valid values are: 1000..9999.

    Returns:
    - dict: A JSON response containing the search results if the request is successful.
    - None: If the request fails or an error occurs.
    '''
    url = "https://api.themoviedb.org/3/search/tv"
    
    # Prepare the parameters for the request
    params = {{
        "query": query,
        "first_air_date_year": first_air_date_year,
        "include_adult": include_adult,
        "language": language,
        "page": page,
        "year": year
    }}
    # Remove parameters that are None
    params = {{k: v for k, v in params.items() if v is not None}}
    
    # Make the API request
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response if successful
    except requests.RequestException:
        return None  # Return None if there is an error


def get_tv_series_details(series_id, append_to_response=None, language="en-US"):
    '''
    Fetches details about a specific TV series.

    Parameters:
    - series_id (int): The ID of the TV series to fetch details for. This is a required parameter.
    - append_to_response (str): A comma-separated list of additional endpoints to include in the response. Optional.
    - language (str): The language code for the response. Default is "en-US".

    Returns:
    - dict: A JSON response containing the TV series details if the request is successful.
    - None: If the request fails or an error occurs.
    '''
    url = f"https://api.themoviedb.org/3/tv/{{series_id}}"
    # Prepare query parameters
    params = {{
        "append_to_response": append_to_response,
        "language": language
    }}
    # Make the API request
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response if successful
    except requests.RequestException:
        return None  # Return None if there is an error

def get_genre_of_show(show_title: str) -> dict:
    '''
    Get the genre of a specific TV show.

    Parameters:
        show_title (str): The title of the TV show for which to retrieve the genre.

    Returns:
        dict: A dictionary containing the genre(s) of the specified TV show. 
              This may include fields such as 'genres', which is a list of genre names. 
              If no genre is found, it may return an empty dictionary or None.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - Place all request parameters within the `params` dictionary; do not format `api_path` using string interpolation or formatted strings.
    '''
    # Step 1. Search for "The Mandalorian" using the /3/search/tv API to find its series_id.
    search_response = search_tv_shows(query=show_title)
    
    # Check if any results were found
    if not search_response.get("results"):
        return {{}}

    # Get the series_id from the response
    series_id = search_response["results"][0]["id"]

    # Step 2. Retrieve detailed information about the show using the /3/tv/{{series_id}} with the acquired series_id to get the genres.
    show_details_response = get_tv_series_details(series_id)

    # Extract genres from the show details
    genres = show_details_response.get("genres", [])

    # Create a dictionary to return genre names
    genre_names = [genre["name"] for genre in genres]

    return {{"genres": genre_names}}

if __name__ == "__main__":
    genre_info = get_genre_of_show(show_title="The Mandalorian")
    print("Genre of The Mandalorian:", genre_info)
```

Now, it's your turn!
### Question: {question}
### Input Code:
```python
{code_solution}
```
### OpenAPI Documents:
{api_doc}
### Output Code:
"""

REUSABLE_ASSEMBLY_MAIN_FUNCTION_TEMPLATE = """You are a coding assistant specializing in Python and API integration. Your task is to translate code snippets with `call_api` placeholders into executable Python code. Each `call_api` placeholder represents an API call that should be implemented as a separate function.

#### Input:
1. A Python code snippet containing one or more `call_api` placeholders.
2. The OpenAPI documentation describing the APIs, including:
   - Endpoints (`path`),
   - Expected input parameters (`parameters`),
   - Response structure (`schema`).

#### Requirements:
1. **Function Creation**: For each API in the OpenAPI specification:
   - First, check if the API's dictionary in the documentation contains a `reusable_code` field. If present:
     - Extract the function code from the `reusable_code` field and reuse it to implement the corresponding API functionality in `call_api`.
     - Make minimal modifications if necessary to integrate the function with the current codebase, while preserving its original logic.
   - If the `reusable_code` field is not present:
     - Implement a Python function using the `requests` library.
     - Use `https://api.themoviedb.org` as the `base_url`. Construct the full URL by appending the `api_path` to this `base_url`.
     - Use the `GET` method for all requests.
     - Include two parameters in the function signature:
       - `params`: An optional dictionary for query parameters.
       - `headers`: A mandatory dictionary containing the following:
         ```python
         headers = {{
             "Authorization": "{api_key}"
         }}
         ```
       - Ensure the function returns parsed response data in a usable format.
2. **Integration**: Replace each `call_api` placeholder in the original code with calls to the corresponding functions, ensuring that the replacement maintains the original logic.
3. **Error Handling**: Add error handling to manage API failures (e.g., HTTP errors). Use `try/except` blocks to log errors or raise exceptions.
4. **Code Quality**:
   - Write clear and descriptive docstrings for each function.
   - Follow Python best practices for readability and maintainability.

#### Additional Notes:
- Validate input parameters where applicable.
- Ensure all requests include the `headers` defined above.
- Clearly document any assumptions made during implementation.
- If reusing functions from the `reusable_code` field, ensure their integration complies with Python conventions and the overall project architecture.

#### Output:
The complete, executable Python code with:
   - Defined functions for each API,
   - Updated logic that calls these functions.

#### Example:
# Question: What is the genre of The Mandalorian?
Input Code:
```python
def get_genre_of_show(show_title: str) -> dict:
    '''
    Get the genre of a specific TV show.

    Parameters:
        show_title (str): The title of the TV show for which to retrieve the genre.

    Returns:
        dict: A dictionary containing the genre(s) of the specified TV show. 
              This may include fields such as 'genres', which is a list of genre names. 
              If no genre is found, it may return an empty dictionary or None.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - Place all request parameters within the `params` dictionary; do not format `api_path` using string interpolation or formatted strings.
    '''
    # Step 1. Search for "The Mandalorian" using the /3/search/tv API to find its series_id.
    search_response = call_api(api_path="/3/search/tv", params={{"query": "The Mandalorian"}})
    
    # Check if any results were found
    if not search_response.get("results"):
        return {{}}

    # Get the series_id from the response
    series_id = search_response["results"][0]["id"]

    # Step 2. Retrieve detailed information about the show using the /3/tv/{{series_id}} with the acquired series_id to get the genres.
    show_details_response = call_api(api_path="/3/tv/{{series_id}}", params={{"series_id": series_id}})

    # Extract genres from the show details
    genres = show_details_response.get("genres", [])

    # Create a dictionary to return genre names
    genre_names = [genre["name"] for genre in genres]

    return {{"genres": genre_names}}

if __name__ == "__main__":
    genre_info = get_genre_of_show(show_title="The Mandalorian")
    print("Genre of The Mandalorian:", genre_info)
```

### Output Code:
```python
import requests

headers = {{
   "Authorization": "{api_key}"
}}

def search_tv_shows(query, first_air_date_year=None, include_adult=False, language="en-US", page=1, year=None):
    '''
    Searches for TV shows based on the provided query and optional parameters.

    Parameters:
    - query (str): The search query for the TV shows. This is a required parameter.
    - first_air_date_year (int, optional): Search only the first air date. Valid values are: 1000..9999.
    - include_adult (bool, optional): Whether to include adult content in the search results. Default is False.
    - language (str, optional): The language code for the response. Default is "en-US".
    - page (int, optional): The page number for pagination. Default is 1.
    - year (int, optional): Search the first air date and all episode air dates. Valid values are: 1000..9999.

    Returns:
    - dict: A JSON response containing the search results if the request is successful.
    - None: If the request fails or an error occurs.
    '''
    url = "https://api.themoviedb.org/3/search/tv"
    
    # Prepare the parameters for the request
    params = {{
        "query": query,
        "first_air_date_year": first_air_date_year,
        "include_adult": include_adult,
        "language": language,
        "page": page,
        "year": year
    }}
    # Remove parameters that are None
    params = {{k: v for k, v in params.items() if v is not None}}
    
    # Make the API request
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response if successful
    except requests.RequestException:
        return None  # Return None if there is an error


def get_tv_series_details(series_id, append_to_response=None, language="en-US"):
    '''
    Fetches details about a specific TV series.

    Parameters:
    - series_id (int): The ID of the TV series to fetch details for. This is a required parameter.
    - append_to_response (str): A comma-separated list of additional endpoints to include in the response. Optional.
    - language (str): The language code for the response. Default is "en-US".

    Returns:
    - dict: A JSON response containing the TV series details if the request is successful.
    - None: If the request fails or an error occurs.
    '''
    url = f"https://api.themoviedb.org/3/tv/{{series_id}}"
    # Prepare query parameters
    params = {{
        "append_to_response": append_to_response,
        "language": language
    }}
    # Make the API request
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response if successful
    except requests.RequestException:
        return None  # Return None if there is an error

def get_genre_of_show(show_title: str) -> dict:
    '''
    Get the genre of a specific TV show.

    Parameters:
        show_title (str): The title of the TV show for which to retrieve the genre.

    Returns:
        dict: A dictionary containing the genre(s) of the specified TV show. 
              This may include fields such as 'genres', which is a list of genre names. 
              If no genre is found, it may return an empty dictionary or None.
    
    Notes:
        - Use the placeholder `call_api(api_path, params)` for each API call
        - Each `call_api` invocation must use an `api_path` that exists in the original toolbox; do not invent or alter paths.
        - Place all request parameters within the `params` dictionary; do not format `api_path` using string interpolation or formatted strings.
    '''
    # Step 1. Search for "The Mandalorian" using the /3/search/tv API to find its series_id.
    search_response = search_tv_shows(query=show_title)
    
    # Check if any results were found
    if not search_response.get("results"):
        return {{}}

    # Get the series_id from the response
    series_id = search_response["results"][0]["id"]

    # Step 2. Retrieve detailed information about the show using the /3/tv/{{series_id}} with the acquired series_id to get the genres.
    show_details_response = get_tv_series_details(series_id)

    # Extract genres from the show details
    genres = show_details_response.get("genres", [])

    # Create a dictionary to return genre names
    genre_names = [genre["name"] for genre in genres]

    return {{"genres": genre_names}}

if __name__ == "__main__":
    genre_info = get_genre_of_show(show_title="The Mandalorian")
    print("Genre of The Mandalorian:", genre_info)
```

Now, it's your turn!
### Question: {question}
### Input:
```python
{code_solution}
```
### OpenAPI Documents as well as a reusable code snippet (optional):
{api_doc}

### Output:
"""

EXECUTION_FAILURE_TEMPLATE = """You were asked to answer the user's question by writing python code to call appreciate APIs and print the final answer.. However, the code execution failed for some reasons. Your task is to analyze the error message and revise the code accordingly. Follow these detailed guidelines:

## Instructions
1. **Syntax Errors**: If the failure is due to syntax issues (e.g., missing arguments), identify the exact location and adjust the code to ensure correct execution.
2. **KeyErrors**: If the error involves a missing key (e.g., when parsing an API response), review the corresponding API's schema and update the implementation to handle the expected structure correctly.
 - If the missing key is from an API response dictionary, review the corresponding API's documentation. Update the code to use the key specified in the documentation, ensuring proper handling of the response.
 - If the missing key is from a dictionary variable defined within the code, modify the code to include the required key in the dictionary or adjust it to use an alternative, existing key.
3. **NoneType Issues**: If the error stems from a `NoneType` (e.g., an API call returning `None`), investigate the function implementation and identify why the API returns an empty value. Modify the code to address this scenario effectively.
4. **API Key Usage**: Avoid using placeholders like `YOUR_API_KEY` in the revised code. Instead, directly use the API key string provided in the original code to ensure the code is functional.
5. **NameError for Placeholder Functions**: If the error involves a NameError such as `NameError: name 'call_api' is not defined`, it indicates that the placeholder function `call_api` was not implemented. In this case:
 - Analyze the user's question and the comments or logic in the existing code.
 - Implement `call_api` as a fully functional API call within a dedicated function.  Ensure the implementation adheres to the correct API specifications.
 - Use this newly defined function in the subsequent code as required to ensure it aligns with the intended logic.

**User Question:**  
{question}

The Python code you previously generated is:  
```python
{python_code}
```
However, the code execution failed with the following result:
============
{execution_result}
============

Using the user's question, the provided code, and the error message as references, generate revised Python code that resolves the issue and successfully accomplishes the user's goal.

Return the revised Python code below:
"""
