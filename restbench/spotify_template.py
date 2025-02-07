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
   - Explicit **Notes** on using `requests_wrapper`, assume an initialized `requests_wrapper` with headers containing the `access_token`. When making network requests:
    - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
    - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
   - Use triple single quotes (`'''`) for the docstring, as shown below.
5. **Function Body**: Leave the function body empty.
6. **Example Execution Block**:
   - Add an `if __name__ == "__main__":` block that demonstrates how to call the function with realistic arguments.
   - Do not include placeholders.
   - Only use specific data available in the input problem and do not make up information that is not in the problem

## Examples:

### Example 1
Here are some example:
Question: Follow all the singers involved in the song See you again
Python Function:
```python
def follow_artists_from_song(song_title: str) -> None:
    '''
    Follows all artists involved in the specified song.

    Parameters:
        song_title (str): The title of the song whose artists should be followed.

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here


if __name__ == "__main__":
    song_title = "See you again"
    follow_artists_from_song(song_title=song_title)
    print(f"I have followed all the singers involved in the song {{song_title}}.")
```

### Example 2
Question: Append the first song of the newest album of my following first artist to my player queue
Python Function:
```python
def add_first_song_of_latest_album_to_queue() -> None:
    '''
    Appends the first song of the newest album of the first artist in the user's following list to their player queue.

    Parameters:
        None

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here


if __name__ == "__main__":
    add_first_song_of_latest_album_to_queue()
    print(
        f"I have appended the first song of the newest album of your following first artist to your player queue."
    )
```

Now, let's begin!
You are given a question: {question}
Python Function:
"""

PLANNER_TEMPLATE_STEP = """Your objective is to analyze the user's complex question and create a breakdown of actionable subtasks, identifying the most appropriate APIs from the provided toolbox to address each subtask in sequence.

### Available Tools:
{toolbox}

Each API includes a request path, request method and a description of its functionality. Utilize these APIs strategically to decompose and solve the user's question. Do not write any code implementation for the steps—only document the subtasks in comments.  Please follow these guidelines:

#### Guidelines
1. **Clarify Requirements**: Carefully read the user's question to determine key requirements, objectives, and expected outcomes. Identify any specific data or information you need to gather to satisfy the request.
2. **Break Down the Task**: Divide the complex task into clear, manageable subtasks that each address part of the user's needs and can be fulfilled using one or more APIs.
3. **Select Relevant APIs**: Match each subtask to the most relevant API(s) from the toolbox. Base your choices on each API's functionality and response format to ensure it provides the required information.
4. **Handle Dependencies**: Check for dependencies between APIs. Make sure to confirm any pre-requisite requirements for the APIs, such as specific IDs or data needed before making a call (e.g., obtaining the correct type and IDs before calling `PUT /me/following`, obtaining the user_id by call GET `/me` bofore calling POST `/users/{{user_id}}/playlists`).
5. **Output in Pseudo-Code**: Write your solution as a Python function using pseudo-code, with each step annotated in comments (for example: "# Step 1. Call GET /search, using the query \"The Dark Side of the Moon\" to find the album's ID.") describing the subtask. **Do not write any code implementation for the steps—only document the subtasks in comments.**

## Below are some example
**Example 1:**
Question: Follow all the singers involved in the song See you again
Pseudo-Code Task:
```python
def follow_artists_from_song(song_title: str) -> None:
    '''
    Follows all artists involved in the specified song.

    Parameters:
        song_title (str): The title of the song whose artists should be followed.

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here

if __name__ == "__main__":
    song_title = "See you again"
    follow_artists_from_song(song_title=song_title)
    print(f"I have followed all the singers involved in the song {{song_title}}.")
```
Planned Subtasks:
```python
def follow_artists_from_song(song_title: str) -> None:
    '''
    Follows all artists involved in the specified song.

    Parameters:
        song_title (str): The title of the song whose artists should be followed.

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here
    # Step 1. Call GET /search to search for the song by its title and retrieve its ID.
    # Step 2. Call GET /tracks/{{id}} to get the artist IDs associated with the specified song.
    # Step 3. Call PUT /me/following to follow each artist using their artist IDs.

if __name__ == "__main__":
    song_title = "See you again"
    follow_artists_from_song(song_title=song_title)
    print(f"I have followed all the singers involved in the song {{song_title}}.")
```

**Example 2:**
Question: Append the first song of the newest album of my following first artist to my player queue
Pseudo-Code Task:
```python
def add_first_song_of_latest_album_to_queue() -> None:
    '''
    Appends the first song of the newest album of the first artist in the user's following list to their player queue.

    Parameters:
        None

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here


if __name__ == "__main__":
    add_first_song_of_latest_album_to_queue()
    print(
        f"I have appended the first song of the newest album of your following first artist to your player queue."
    )
```
Planned Subtasks:
```python
def add_first_song_of_latest_album_to_queue() -> None:
    '''
    Appends the first song of the newest album of the first artist in the user's following list to their player queue.

    Parameters:
        None

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here
    # Step 1. Call GET /me/following to retrieve the user's following list and identify the first artist.
    # Step 2. Call GET /artists/{{id}}/albums to fetch the albums of the first artist and determine their newest album.
    # Step 3. Call GET /albums/{{id}}/tracks to get the track list of the newest album and extract the ID of the first song.
    # Step 4. Call POST /me/player/queue to add the identified song to the user's player queue.


if __name__ == "__main__":
    add_first_song_of_latest_album_to_queue()
    print(
        f"I have appended the first song of the newest album of your following first artist to your player queue."
    )
```

Now, let's begin!
**User's Question**: {question}
**Pseudo-Code Task**:
```python
{pseudo_code_task}
```
Planned Subtasks:
"""

# FUNCTION_TEMPLATE = """Your task is to assist the user in selecting appropriate APIs from the provided toolbox and completing the function template to solve the problem accurately.

# ## Instructions

# 1. **Inputs Provided**:
#    - **Problem Description**: A specific question or request from the user (e.g., "give me the number of movies directed by Sofia Coppola").
#    - **Pseudo-Code Task Template**: A function template containing:
#      - Function signature, parameters, return type, and a functional description.
#      - Structured subtask comments directly embedded in the pseudo-code template, outlining each planned subtask step-by-step.
#    - **API Documentation**: A detailed list of APIs, including their parameters, usage instructions, and output format schema.

# 2. **Expected Output**:
#    - Complete the pseudo-code template by selecting and integrating the most suitable API calls from the provided toolbox.
#    - Use the provided API documentation as a guide to ensure each API call adheres to the documented specifications, including:
#      - Correct usage of input parameters.
#      - Accurate handling of the response format, including field names and types.

# 3. **Guidelines for API Parameter Handling**:
#    - **Extract Parameter Information**: Analyze the API documentation to extract the full list of required and optional parameters for each API.
#    - **Map Input Data to Parameters**: Ensure all required parameters are correctly populated using the provided inputs or logical derivations. For optional parameters, decide their necessity based on the problem context.
#    - **Validate Completeness**: Confirm that no required parameters are missing or incorrectly formatted before constructing the API request.

# 4. **Guidelines for API Response Handling**:
#    - **Refer to API Schema**: Use the API documentation to understand the structure and types of the response fields. Ensure the code only accesses fields explicitly described in the schema.
#    - **Avoid Nonexistent Fields**: Do not reference fields that are not documented, even if they might appear in example responses.
#    - **Type Safety**: Handle type-specific operations (e.g., casting, conditional checks) based on the documented data types of the response fields.

# 5. **Assumptions for Network Requests**:
#    - Use the initialized `requests_wrapper` with headers containing the `access_token`.
#    - When making network requests:
#      - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if applicable.
#      - Use `requests_wrapper.post(url, data=data)`, `requests_wrapper.put(url, data=data)`, or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.

# 6. **Logical API Integration**:
#    - Ensure the sequence of API calls logically aligns with the problem requirements.
#    - Include any necessary preliminary calls (e.g., fetching an entity ID) to facilitate subsequent steps.
#    - Add clear and concise comments to explain the purpose of each API call and how it contributes to the overall task.

# 7. **Constraints**:
#    - Do not directly answer the user's problem. Instead, complete the pseudo-code to enable accurate task execution using the APIs.
#    - Ensure the function template is logically consistent, complete, and ready for execution without redundant steps.

# ## Example Scenarios:
# **Example 1:**
# Question: Follow all the singers involved in the song See you again
# Pseudo-Code Task:
# ```python
# def follow_artists_from_song(song_title: str) -> None:
#     '''
#     Follows all artists involved in the specified song.

#     Parameters:
#         song_title (str): The title of the song whose artists should be followed.

#     Return:
#         None: The function does not return anything.

#     Notes:
#         - This function uses the `requests_wrapper` for network requests.
#         - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
#             - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
#             - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
#     '''
#     # Function logic goes here
#     # Step 1. Call GET /search to search for the song by its title and retrieve its ID.
#     # Step 2. Call GET /tracks/{{id}} to get the artist IDs associated with the specified song.
#     # Step 3. Call PUT /me/following to follow each artist using their artist IDs.

# if __name__ == "__main__":
#     song_title = "See you again"
#     follow_artists_from_song(song_title=song_title)
#     print(f"I have followed all the singers involved in the song {{song_title}}.")
# ```

# Pseudo-Code Solution:
# ```python
# def follow_artists_from_song(song_title: str) -> None:
#     '''
#     Follows all artists involved in the specified song.

#     Parameters:
#         song_title (str): The title of the song whose artists should be followed.

#     Return:
#         None: The function does not return anything.

#     Notes:
#         - This function uses the `requests_wrapper` for network requests.
#         - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
#             - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
#             - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
#     '''
#     # Step 1: Search for the song "When You Believe"
#     search_results = requests_wrapper.get(
#         "https://api.spotify.com/v1/search",
#         params={{"q": song_title, "type": "track", "limit": 1}},
#     ).json()

#     # Step 2. Extract the track ID and the artists' IDs
#     track = search_results["tracks"]["items"][0]
#     track_id = track["id"]
#     artists = track["artists"]
#     artist_ids = [artist["id"] for artist in artists]

#     # Step 3. Call PUT /me/following to follow each artist using their artist IDs.
#     follow_response = requests_wrapper.put(
#         "https://api.spotify.com/v1/me/following",
#         params={{"type": "artist", "ids": ",".join(artist_ids)}},
#         data={{"type": "artist", "ids": ",".join(artist_ids)}},
#     )

#     # Check response status
#     if follow_response.status_code == 204:
#         print(f"Successfully followed all artists involved in the song {{song_title}}.")
#     else:
#         print(f"Failed to follow artists: {{follow_response.json()}}")

# if __name__ == "__main__":
#     song_title = "See you again"
#     follow_artists_from_song(song_title=song_title)
# ```

# **Example 2:**
# Question: Append the first song of the newest album of my following first artist to my player queue
# Pseudo-Code Task:
# ```python
# def add_first_song_of_latest_album_to_queue() -> None:
#     '''
#     Appends the first song of the newest album of the first artist in the user's following list to their player queue.

#     Parameters:
#         None

#     Return:
#         None: The function does not return anything.

#     Notes:
#         - This function uses the `requests_wrapper` for network requests.
#         - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
#             - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
#             - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
#     '''
#     # Function logic goes here
#     # Step 1. Call GET /me/following to retrieve the user's following list and identify the first artist.
#     # Step 2. Call GET /artists/{{id}}/albums to fetch the albums of the first artist and determine their newest album.
#     # Step 3. Call GET /albums/{{id}}/tracks to get the track list of the newest album and extract the ID of the first song.
#     # Step 4. Call POST /me/player/queue to add the identified song to the user's player queue.

# if __name__ == "__main__":
#     add_first_song_of_latest_album_to_queue()
#     print(
#         f"I have appended the first song of the newest album of your following first artist to your player queue."
#     )
# ```

# Pseudo-Code Solution:
# ```python
# def add_first_song_of_latest_album_to_queue() -> None:
#     '''
#     Appends the first song of the newest album of the first artist in the user's following list to their player queue.

#     Parameters:
#         None

#     Return:
#         None: The function does not return anything.

#     Notes:
#         - This function uses the `requests_wrapper` for network requests.
#         - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
#             - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
#             - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
#     '''
#     # Step 1. Call GET /me/following to retrieve the user's following list and identify the first artist.
#     # # Get the current user's followed artists
#     followed_info = requests_wrapper.get(
#         "https://api.spotify.com/v1/me/following", params={{"type": "artist"}}
#     ).json()
#     followed_artists = followed_info["artists"]["items"]
#     # Get the ID of the first followed artist
#     first_artist_id = followed_artists[0]["id"]

#     # Step 2. Call GET /artists/{{id}}/albums to fetch the albums of the first artist and determine their newest album.
#     # Get the albums of the first followed artist
#     albums = requests_wrapper.get(
#         f"https://api.spotify.com/v1/artists/{{first_artist_id}}/albums"
#     ).json()["items"]
#     # Find the newest album (assuming the first album in the list is the newest)
#     newest_album_id = albums[0]["id"]

#     # Step 3. Call GET /albums/{{id}}/tracks to get the track list of the newest album and extract the ID of the first song.
#     # Get the tracks of the newest album
#     tracks = requests_wrapper.get(
#         f"https://api.spotify.com/v1/albums/{{newest_album_id}}/tracks"
#     ).json()["items"]

#     # Get the URI of the first track from the newest album
#     first_track_uri = tracks[0]["uri"]

#     # Step 4. Call POST /me/player/queue to add the identified song to the user's player queue.
#     # Add that track to the user's player queue
#     requests_wrapper.post(
#         "https://api.spotify.com/v1/me/player/queue",
#         data=json.dumps({{"uri": first_track_uri}}),
#     )

#     print("First song of the newest album added to the player queue.")

# if __name__ == "__main__":
#     add_first_song_of_latest_album_to_queue()
# ```

# ## Provided API toolbox:
# {toolbox}

# Let's begin!
# Question: {question}
# Pseudo-Code Task:
# {pseudo_code_task}
# Please complete the pseudo-code solution:
# """


FUNCTION_TEMPLATE = """Your task is to assist the user in selecting the right APIs from the toolbox and completing a function template to accurately address their problem.

#### Key Steps and Requirements:

1. **Provided Inputs**:
   - **Problem Description**: A clear user query or request (e.g., "List all movies directed by Sofia Coppola").
   - **Pseudo-Code Template**: Includes function signature, parameters, return type, and detailed subtask comments.
   - **API Documentation**: Describes APIs, including their parameters, `requestBody` fields (if applicable), usage instructions, and output schemas.

2. **Expected Output**:
   - Complete the template by integrating the appropriate API calls.
   - Follow all documented API specifications:
     - Accurately map query parameters to API request `params`.
     - For POST/PUT/DELETE requests, populate the `data` field using the `requestBody` schema and examples in their API documentations.

3. **API Parameter and `requestBody` Guidelines**:
   - Extract all required and optional fields for each API:
     - Use `params` for query parameters.
     - Use `data` for fields described under `requestBody` for POST/PUT/DELETE requests. Refer to the provided schema and examples to structure the `data` content accurately.
   - Validate completeness and formatting before constructing requests.

4. **API Response Handling**:
   - Refer strictly to the documented response schema.
   - Avoid using undocumented fields.
   - Ensure type-safe operations (e.g., casting, conditional checks).

5. **Network Request Requirements**:
   - Use the initialized `requests_wrapper` with headers containing the `access_token`.
   - Follow these request formats:
     - **GET**: `requests_wrapper.get(url, params=params)`.
     - **POST/PUT/DELETE**: `requests_wrapper.[method](url, data=data)`.

6. **Integration Logic**:
   - Sequence API calls logically to achieve the desired results.
   - Include preparatory API calls if required (e.g., fetching an entity ID).
   - Add concise comments explaining the purpose of each step.

7. **Constraints**:
   - Do not directly solve the user’s query; focus on completing the function template.
   - Ensure the template is executable, logically consistent, and avoids redundancy.


## Example Scenarios:
**Example 1:**
Question: Follow all the singers involved in the song See you again
Pseudo-Code Task:
```python
def follow_artists_from_song(song_title: str) -> None:
    '''
    Follows all artists involved in the specified song.

    Parameters:
        song_title (str): The title of the song whose artists should be followed.

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here
    # Step 1. Call GET /search to search for the song by its title and retrieve its ID.
    # Step 2. Call GET /tracks/{{id}} to get the artist IDs associated with the specified song.
    # Step 3. Call PUT /me/following to follow each artist using their artist IDs.

if __name__ == "__main__":
    song_title = "See you again"
    follow_artists_from_song(song_title=song_title)
    print(f"I have followed all the singers involved in the song {{song_title}}.")
```

Pseudo-Code Solution:
```python
def follow_artists_from_song(song_title: str) -> None:
    '''
    Follows all artists involved in the specified song.

    Parameters:
        song_title (str): The title of the song whose artists should be followed.

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Step 1: Search for the song "When You Believe"
    search_results = requests_wrapper.get(
        "https://api.spotify.com/v1/search",
        params={{"q": song_title, "type": "track", "limit": 1}},
    ).json()

    # Step 2. Extract the track ID and the artists' IDs
    track = search_results["tracks"]["items"][0]
    track_id = track["id"]
    artists = track["artists"]
    artist_ids = [artist["id"] for artist in artists]
    
    # Step 3. Call PUT /me/following to follow each artist using their artist IDs.
    follow_response = requests_wrapper.put(
        "https://api.spotify.com/v1/me/following",
        params={{"type": "artist", "ids": ",".join(artist_ids)}},
        data={{"type": "artist", "ids": ",".join(artist_ids)}},
    )
    
    # Check response status
    if follow_response.status_code == 204:
        print(f"Successfully followed all artists involved in the song {{song_title}}.")
    else:
        print(f"Failed to follow artists: {{follow_response.json()}}")

if __name__ == "__main__":
    song_title = "See you again"
    follow_artists_from_song(song_title=song_title)
```

**Example 2:**
Question: Append the first song of the newest album of my following first artist to my player queue
Pseudo-Code Task:
```python
def add_first_song_of_latest_album_to_queue() -> None:
    '''
    Appends the first song of the newest album of the first artist in the user's following list to their player queue.

    Parameters:
        None

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here
    # Step 1. Call GET /me/following to retrieve the user's following list and identify the first artist.
    # Step 2. Call GET /artists/{{id}}/albums to fetch the albums of the first artist and determine their newest album.
    # Step 3. Call GET /albums/{{id}}/tracks to get the track list of the newest album and extract the ID of the first song.
    # Step 4. Call POST /me/player/queue to add the identified song to the user's player queue.

if __name__ == "__main__":
    add_first_song_of_latest_album_to_queue()
    print(
        f"I have appended the first song of the newest album of your following first artist to your player queue."
    )
```

Pseudo-Code Solution:
```python
def add_first_song_of_latest_album_to_queue() -> None:
    '''
    Appends the first song of the newest album of the first artist in the user's following list to their player queue.

    Parameters:
        None

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Step 1. Call GET /me/following to retrieve the user's following list and identify the first artist.
    # # Get the current user's followed artists
    followed_info = requests_wrapper.get(
        "https://api.spotify.com/v1/me/following", params={{"type": "artist"}}
    ).json()
    followed_artists = followed_info["artists"]["items"]
    # Get the ID of the first followed artist
    first_artist_id = followed_artists[0]["id"]

    # Step 2. Call GET /artists/{{id}}/albums to fetch the albums of the first artist and determine their newest album.
    # Get the albums of the first followed artist
    albums = requests_wrapper.get(
        f"https://api.spotify.com/v1/artists/{{first_artist_id}}/albums"
    ).json()["items"]
    # Find the newest album (assuming the first album in the list is the newest)
    newest_album_id = albums[0]["id"]

    # Step 3. Call GET /albums/{{id}}/tracks to get the track list of the newest album and extract the ID of the first song.
    # Get the tracks of the newest album
    tracks = requests_wrapper.get(
        f"https://api.spotify.com/v1/albums/{{newest_album_id}}/tracks"
    ).json()["items"]

    # Get the URI of the first track from the newest album
    first_track_uri = tracks[0]["uri"]

    # Step 4. Call POST /me/player/queue to add the identified song to the user's player queue.
    # Add that track to the user's player queue
    requests_wrapper.post(
        "https://api.spotify.com/v1/me/player/queue",
        data=json.dumps({{"uri": first_track_uri}}),
    )

    print("First song of the newest album added to the player queue.")

if __name__ == "__main__":
    add_first_song_of_latest_album_to_queue()
```

## Provided API toolbox:
{toolbox}

Let's begin!
Question: {question}
Pseudo-Code Task:
{pseudo_code_task}
Please complete the pseudo-code solution:
"""

REPLAN_TEMPLATE = """Your task is to revise the provided pseudo-code solution to address issues in the original plan, including empty results or invalid API usage, by leveraging available APIs from the toolbox.

### Available Tools:
{toolbox}

### Background
- A pseudo-code solution has already been provided, but it has issues:
  1. The solution returns an empty result or fails to address the user's question.
  2. The solution references APIs that are not part of the provided toolbox (invalid APIs).
- Your task is to replan the solution by replacing invalid or missing APIs with valid ones while preserving the original logic.

### Input
1. **Original Question**: The user's original request or problem.
2. **Initial Code Solution**: The previous pseudo-code plan, annotated with comments explaining the intended steps but containing errors or gaps.
3. **Feedback on Initial Solution**: Includes:
   - A description of issues in the initial solution (e.g., empty result, use of invalid APIs).
   - A list of invalid APIs and potential alternatives from the toolbox.
4. **Available Tools**: A curated list of valid APIs, including:
   - API names, paths, and descriptions.
   - Example usages and parameter details.

### Expected Output
- A corrected pseudo-code solution (within the block of ```python[YOUR CODE]```) that:
  1. Ensures every API call strictly matches an API from the toolbox.
  2. Resolves the feedback issues by appropriately replanning steps using valid APIs.
  3. Maintains the original logical flow of the solution.
- Annotate the pseudo-code with comments explaining:
  - The purpose of each step.
  - How the new API call addresses the user’s question.

### Constraints
- Do not alter the overall structure or purpose of the solution.
- Ensure the replanned solution directly addresses the user’s question and resolves the identified issues.
- Clearly explain how each change aligns with the feedback and maintains logical consistency.

### Here are some examples
#### Example 1:
**Question**: Append the first song of the newest album of my following first artist to my player queue
**Initial Code Solution**:
```python
def add_first_song_of_latest_album_to_queue() -> None:
    '''
    Appends the first song of the newest album of the first artist in the user's following list to their player queue.

    Return:
        None: The function does not return anything.
    '''
    # Step 1. Get the list of artists that the user is following
    params = {{"limit": 1}}  # We only need the first artist
    response = requests_wrapper.get("/me/following", params=params)
    following_artists = response.json()["artists"]["items"]

    # Step 2. Get the first artist from the list
    artist_id = following_artists[0]["id"]

    # Step 3. Get the latest album of this artist
    response = requests_wrapper.get(f"/artists/{{artist_id}}/albums")
    albums = response.json()["items"]
    latest_album_id = max(albums, key=lambda x: x["release_date"]).["id"]

    # Step 4. Get the first track of this album
    response = requests_wrapper.get(f"/albums/{{latest_album_id}}/tracks")
    tracks = response.json()["items"]
    first_track_id = tracks[0]["id"]

    # Step 5. Add this track to the user's player queue
    data = {{"uris": [first_track_id]}}
    requests_wrapper.post("/me/player/queue", data=data)
```
*Problem Feedback**:
No planning content described by comments was detected in the code. Please ensure that the planning results are provided in the form of comments instead of implementing specific functions.

**Corrected Code Solution**:
```python
def add_first_song_of_latest_album_to_queue() -> None:
    '''
    Appends the first song of the newest album of the first artist in the user's following list to their player queue.

    Parameters:
        None

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Step 1. Call GET /me/following to retrieve the list of artists the user follows. Extract the ID of the first artist.
    # Step 2. Call GET /artists/{{id}}/albums to fetch the newest album. Extract the album's ID.
    # Step 3. Call GET /albums/{{id}}/tracks to get the list of tracks in the album. Extract the URI of the first track.
    # Step 4. Call POST /me/player/queue to add it to the user's playback queue.

if __name__ == "__main__":
    add_first_song_of_latest_album_to_queue()
    print(
        f"I have appended the first song of the newest album of your following first artist to your player queue."
    )
```


#### Example 2:
**Question**: Give me a song of my favorite artist
**Initial Code Solution**:
```python
def get_favorite_artist_song() -> str:
    '''
    Retrieves a song from the user's favorite artist.

    Parameters:
        None

    Return:
        str: The title of a song by the favorite artist.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''

    # Step 1. Call GET /me/top/artists to retrieve the user's top artists and find the ID of the favorite artist.
    # Step 2. Call GET /artists/{{id}}/top-tracks to get the top tracks for the favorite artist using their Spotify ID.
    # Step 3. Extract and return the title of one song from the list of the artist's top tracks.

if __name__ == "__main__":
    song = get_favorite_artist_song()
    print(f"I have retrieved a song from your favorite artist.")
```
*Problem Feedback**:
The `/me/top/artists` API is invalid as it is not existed in the provided toolbox. Please check it and replace it with an appropriate one. 

**Corrected Code Solution**:
```python
def get_favorite_artist_song() -> str:
    '''
    Retrieves a song from the user's favorite artist.

    Parameters:
        None

    Return:
        str: The title of a song by the favorite artist.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''

    # Step 1. Call GET /me/top/{{type}} to retrieve the user's top artists and find the ID of the favorite artist.
    # Step 2. Call GET /artists/{{id}} to get a track for the favorite artist using their Spotify ID.
    # Step 3. Extract and return the title of one song from the list of the artist's top tracks.

if __name__ == "__main__":
    song = get_favorite_artist_song()
    print(f"I have retrieved a song from your favorite artist.")
```

Now it is your turn!
**Question**: {question}
**Initial Code Solution**:
```python
{pseudo_code_solution}
```
*Problem Feedback**:
{feedback}
**Corrected Code Solution**:
"""

EXECUTION_FAILURE_TEMPLATE = """You were asked to answer the user's question by writing python code to call appreciate APIs and print the final answer.. However, the code execution failed for some reasons. Your task is to analyze the error message and revise the code accordingly. Follow these detailed guidelines:

## Instructions
1. **Syntax Errors**: If the failure is due to syntax issues (e.g., missing arguments), identify the exact location and adjust the code to ensure correct execution.
2. **TypeError**: If the error involves a missing key (e.g., when parsing an API response), review the corresponding API's schema and update the implementation to handle the expected structure correctly.
    - If the missing key is from an API response dictionary, review the corresponding API's documentation. Update the code to use the key specified in the documentation, ensuring proper handling of the response.
    - If the missing key is from a dictionary variable defined within the code, modify the code to include the required key in the dictionary or adjust it to use an alternative, existing key.
    - If a TypeError indicates that a required positional argument is missing (e.g., `TypeError: post() missing 1 required positional argument: 'data'`), ensure the missing argument is included in the function call. For HTTP requests, if no meaningful data exists to send, include an empty object such as `data = {{}}`.
3. **JSONDecodeError**: If an API's JSON response raises the error `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`, this indicates the API response is empty. In such cases, print a message stating that the API's response is empty and terminate further execution.


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

REUSABLE_FUNCTION_TEMPLATE = """
Your task is to assist the user in selecting the right APIs from the toolbox and completing a function template to accurately address their problem.

#### Key Steps and Requirements:

1. **Provided Inputs**:
   - **Problem Description**: A clear user query or request (e.g., "List all movies directed by Sofia Coppola").
   - **Pseudo-Code Template**: Includes function signature, parameters, return type, and detailed subtask comments.
   - **API Documentation**: Describes APIs, including their parameters, `requestBody` fields (if applicable), usage instructions, and output schemas.
     - May also include an `implementation_example` field (possibly empty) containing Python code snippets demonstrating API usage.

2. **Expected Output**:
   - Complete the template by integrating the appropriate API calls.
   - Follow all documented API specifications:
     - Accurately map query parameters to API request `params`.
     - For POST/PUT/DELETE requests, populate the `data` field using the `requestBody` schema and examples in their API documentation.
     - Leverage any provided `implementation_example` code snippets to ensure the correctness and best practices in API calls.

3. **API Parameter and `requestBody` Guidelines**:
   - Extract all required and optional fields for each API:
     - Use `params` for query parameters.
     - Use `data` for fields described under `requestBody` for POST/PUT/DELETE requests. Refer to the provided schema and examples to structure the `data` content accurately.
   - Validate completeness and formatting before constructing requests.

4. **API Response Handling**:
   - Refer strictly to the documented response schema.
   - Avoid using undocumented fields.
   - Ensure type-safe operations (e.g., casting, conditional checks).

5. **Network Request Requirements**:
   - Use the initialized `requests_wrapper` with headers containing the `access_token`.
   - Follow these request formats:
     - **GET**: `requests_wrapper.get(url, params=params)`.
     - **POST/PUT/DELETE**: `requests_wrapper.[method](url, data=data)`.

6. **Incorporating `implementation_example`**:
   - If an `implementation_example` field is provided in the API documentation, carefully examine and adapt the code snippets.
   - Ensure the final implementation aligns with the demonstrated best practices, including handling errors and edge cases as illustrated.

7. **Integration Logic**:
   - Sequence API calls logically to achieve the desired results.
   - Include preparatory API calls if required (e.g., fetching an entity ID).
   - Add concise comments explaining the purpose of each step.

8. **Constraints**:
   - Do not directly solve the user’s query; focus on completing the function template.
   - Ensure the template is executable, logically consistent, and avoids redundancy.

## Example Scenarios:
**Example 1:**
Question: Follow all the singers involved in the song See you again
Pseudo-Code Task:
```python
def follow_artists_from_song(song_title: str) -> None:
    '''
    Follows all artists involved in the specified song.

    Parameters:
        song_title (str): The title of the song whose artists should be followed.

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here
    # Step 1. Call GET /search to search for the song by its title and retrieve its ID.
    # Step 2. Call GET /tracks/{{id}} to get the artist IDs associated with the specified song.
    # Step 3. Call PUT /me/following to follow each artist using their artist IDs.

if __name__ == "__main__":
    song_title = "See you again"
    follow_artists_from_song(song_title=song_title)
    print(f"I have followed all the singers involved in the song {{song_title}}.")
```

Pseudo-Code Solution:
```python
def follow_artists_from_song(song_title: str) -> None:
    '''
    Follows all artists involved in the specified song.

    Parameters:
        song_title (str): The title of the song whose artists should be followed.

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Step 1: Search for the song "When You Believe"
    search_results = requests_wrapper.get(
        "https://api.spotify.com/v1/search",
        params={{"q": song_title, "type": "track", "limit": 1}},
    ).json()

    # Step 2. Extract the track ID and the artists' IDs
    track = search_results["tracks"]["items"][0]
    track_id = track["id"]
    artists = track["artists"]
    artist_ids = [artist["id"] for artist in artists]
    
    # Step 3. Call PUT /me/following to follow each artist using their artist IDs.
    follow_response = requests_wrapper.put(
        "https://api.spotify.com/v1/me/following",
        params={{"type": "artist", "ids": ",".join(artist_ids)}},
        data={{"type": "artist", "ids": ",".join(artist_ids)}},
    )
    
    # Check response status
    if follow_response.status_code == 204:
        print(f"Successfully followed all artists involved in the song {{song_title}}.")
    else:
        print(f"Failed to follow artists: {{follow_response.json()}}")

if __name__ == "__main__":
    song_title = "See you again"
    follow_artists_from_song(song_title=song_title)
```

**Example 2:**
Question: Append the first song of the newest album of my following first artist to my player queue
Pseudo-Code Task:
```python
def add_first_song_of_latest_album_to_queue() -> None:
    '''
    Appends the first song of the newest album of the first artist in the user's following list to their player queue.

    Parameters:
        None

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Function logic goes here
    # Step 1. Call GET /me/following to retrieve the user's following list and identify the first artist.
    # Step 2. Call GET /artists/{{id}}/albums to fetch the albums of the first artist and determine their newest album.
    # Step 3. Call GET /albums/{{id}}/tracks to get the track list of the newest album and extract the ID of the first song.
    # Step 4. Call POST /me/player/queue to add the identified song to the user's player queue.

if __name__ == "__main__":
    add_first_song_of_latest_album_to_queue()
    print(
        f"I have appended the first song of the newest album of your following first artist to your player queue."
    )
```

Pseudo-Code Solution:
```python
def add_first_song_of_latest_album_to_queue() -> None:
    '''
    Appends the first song of the newest album of the first artist in the user's following list to their player queue.

    Parameters:
        None

    Return:
        None: The function does not return anything.

    Notes:
        - This function uses the `requests_wrapper` for network requests.
        - Assumes that the `requests_wrapper` is initialized and contains the necessary `access_token` in its headers.
            - Use `requests_wrapper.get(url, params=params)` for GET requests, where `params` is optional and should contain query parameters if provided.
            - Use `requests_wrapper.post(url, data=data)` or `requests_wrapper.put(url, data=data)` or `requests_wrapper.delete(url, data=data)` for POST, PUT, and DELETE requests, respectively. The `data` parameter is optional and should contain request body data if provided.
    '''
    # Step 1. Call GET /me/following to retrieve the user's following list and identify the first artist.
    # # Get the current user's followed artists
    followed_info = requests_wrapper.get(
        "https://api.spotify.com/v1/me/following", params={{"type": "artist"}}
    ).json()
    followed_artists = followed_info["artists"]["items"]
    # Get the ID of the first followed artist
    first_artist_id = followed_artists[0]["id"]

    # Step 2. Call GET /artists/{{id}}/albums to fetch the albums of the first artist and determine their newest album.
    # Get the albums of the first followed artist
    albums = requests_wrapper.get(
        f"https://api.spotify.com/v1/artists/{{first_artist_id}}/albums"
    ).json()["items"]
    # Find the newest album (assuming the first album in the list is the newest)
    newest_album_id = albums[0]["id"]

    # Step 3. Call GET /albums/{{id}}/tracks to get the track list of the newest album and extract the ID of the first song.
    # Get the tracks of the newest album
    tracks = requests_wrapper.get(
        f"https://api.spotify.com/v1/albums/{{newest_album_id}}/tracks"
    ).json()["items"]

    # Get the URI of the first track from the newest album
    first_track_uri = tracks[0]["uri"]

    # Step 4. Call POST /me/player/queue to add the identified song to the user's player queue.
    # Add that track to the user's player queue
    requests_wrapper.post(
        "https://api.spotify.com/v1/me/player/queue",
        data=json.dumps({{"uri": first_track_uri}}),
    )

    print("First song of the newest album added to the player queue.")

if __name__ == "__main__":
    add_first_song_of_latest_album_to_queue()
```

## Provided API toolbox:
{toolbox}

Let's begin!
Question: {question}
Pseudo-Code Task:
{pseudo_code_task}
Please complete the pseudo-code solution:
"""
