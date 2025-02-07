import json

"""Quick and dirty representation for OpenAPI specs."""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Union


def dereference_refs(spec_obj: dict, full_spec: dict) -> Union[dict, list]:
    """Try to substitute $refs.

    The goal is to get the complete docs for each endpoint in context for now.

    In the few OpenAPI specs I studied, $refs referenced models
    (or in OpenAPI terms, components) and could be nested. This code most
    likely misses lots of cases.
    """

    def _retrieve_ref_path(path: str, full_spec: dict) -> dict:
        components = path.split("/")
        if components[0] != "#":
            raise RuntimeError(
                "All $refs I've seen so far are uri fragments (start with hash)."
            )
        out = full_spec
        for component in components[1:]:
            out = out[component]
        return out

    def _dereference_refs(
        obj: Union[dict, list], stop: bool = False
    ) -> Union[dict, list]:
        if stop:
            return obj
        obj_out: Dict[str, Any] = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "$ref":
                    # stop=True => don't dereference recursively.
                    return _dereference_refs(
                        _retrieve_ref_path(v, full_spec), stop=False
                    )
                elif isinstance(v, list):
                    obj_out[k] = [_dereference_refs(el) for el in v]
                elif isinstance(v, dict):
                    obj_out[k] = _dereference_refs(v)
                else:
                    obj_out[k] = v
            return obj_out
        elif isinstance(obj, list):
            return [_dereference_refs(el) for el in obj]
        else:
            return obj

    return _dereference_refs(spec_obj)


def merge_allof_properties(obj):
    def merge(to_merge):
        merged = {"properties": {}, "required": [], "type": "object"}
        for partial_schema in to_merge:
            if "allOf" in partial_schema:
                tmp = merge(partial_schema["allOf"])
                merged["properties"].update(tmp["properties"])
                if "required" in tmp:
                    merged["required"].extend(tmp["required"])
                continue
            if "properties" in partial_schema:
                merged["properties"].update(partial_schema["properties"])
            if "required" in partial_schema:
                merged["required"].extend(partial_schema["required"])
        return merged

    def _merge_allof(obj):
        obj_out = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "allOf":
                    return _merge_allof(merge(v))
                elif isinstance(v, list):
                    obj_out[k] = [_merge_allof(el) for el in v]
                elif isinstance(v, dict):
                    obj_out[k] = _merge_allof(v)
                else:
                    obj_out[k] = v
            return obj_out
        elif isinstance(obj, list):
            return [_merge_allof(el) for el in obj]
        else:
            return obj

    return _merge_allof(obj)


@dataclass
class ReducedOpenAPISpec:
    servers: List[dict]
    description: str
    endpoints: List[Tuple[str, Union[str, None], dict]]


def reduce_openapi_spec(
    spec: dict,
    dereference: bool = True,
    only_required: bool = True,
    merge_allof: bool = False,
) -> ReducedOpenAPISpec:
    """Simplify/distill/minify a spec somehow.

    I want a smaller target for retrieval and (more importantly)
    I want smaller results from retrieval.
    I was hoping https://openapi.tools/ would have some useful bits
    to this end, but doesn't seem so.
    """
    # 1. Consider only get, post, patch, delete endpoints.
    endpoints = [
        (f"{operation_name.upper()} {route}", docs.get("description"), docs)
        for route, operation in spec["paths"].items()
        for operation_name, docs in operation.items()
        if operation_name in ["get", "post", "patch", "delete", "put"]
    ]

    # endpoints = []
    # for route, operation in spec["paths"].items():
    #     for operation_name, docs in operation.items():
    #         if operation_name in ["get", "post", "patch", "delete"]:
    #             if "parameters" in operation:
    #                 if "parameters" in operation:
    #                     docs += operation["parameters"]
    #                 else:
    #                     docs = operation["parameters"]
    #             endpoints.append(
    #                 (f"{operation_name.upper()} {route}", docs.get("description"), docs)
    #             )

    # 2. Replace any refs so that complete docs are retrieved.
    # Note: probably want to do this post-retrieval, it blows up the size of the spec.
    if dereference:
        endpoints = [
            (name, description, dereference_refs(docs, spec))
            for name, description, docs in endpoints
        ]

    # 3. Merge "allof" properties. Maybe very slow.
    if merge_allof:
        endpoints = [
            (name, description, merge_allof_properties(docs))
            for name, description, docs in endpoints
        ]

    # 3. Strip docs down to required request args + happy path response.
    def reduce_endpoint_docs(docs: dict) -> dict:
        out = {}
        if docs.get("description"):
            out["description"] = docs.get("description")
        if docs.get("parameters"):
            if only_required:
                out["parameters"] = [
                    parameter
                    for parameter in docs.get("parameters", [])
                    if parameter.get("required")
                ]
            else:
                out["parameters"] = [
                    parameter for parameter in docs.get("parameters", [])
                ]
        if docs.get("requestBody"):
            out["requestBody"] = docs.get("requestBody")
        if "200" in docs["responses"]:
            out["responses"] = docs["responses"]["200"]
        elif 200 in docs["responses"]:
            out["responses"] = docs["responses"][200]
        return out

    endpoints = [
        (name, description, reduce_endpoint_docs(docs))
        for name, description, docs in endpoints
    ]
    return ReducedOpenAPISpec(
        servers=spec["servers"],
        description=spec["info"].get("description", ""),
        endpoints=endpoints,
    )


def init_spotify(requests_wrapper):
    # WARNING: this will remove all your data from spotify!!!
    # The final environment:
    # Your Music: 6 tracks, top-3 tracks of Lana Del Rey and Whitney Houston
    # Your Albums: Born To Die by Lana Del Rey and reputation by Taylor Swift
    # Your Playlists: My R&B with top-3 tracks of Whitney Houston and My Rock with top-3 tracks of Beatles
    # Your Followed Artists: Lana Del Rey, Whitney Houston, and Beatles
    # Current Playing: album Born To Die by Lana Del Rey

    user_id = json.loads(requests_wrapper.get("https://api.spotify.com/v1/me").text)[
        "id"
    ]

    # remove all playlists, DONE
    playlist_ids = json.loads(
        requests_wrapper.get("https://api.spotify.com/v1/me/playlists").text
    )["items"]
    playlist_ids = [playlist["id"] for playlist in playlist_ids]
    for playlist_id in playlist_ids:
        requests_wrapper.delete(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/followers"
        )

    # remove all tracks from my music, DONE
    track_ids = json.loads(
        requests_wrapper.get("https://api.spotify.com/v1/me/tracks").text
    )["items"]
    if len(track_ids) != 0:
        track_ids = [track["track"]["id"] for track in track_ids]
        requests_wrapper.delete(
            f'https://api.spotify.com/v1/me/tracks?ids={",".join(track_ids)}'
        )

    # remove all albums from my music
    album_items = requests_wrapper.get("https://api.spotify.com/v1/me/albums").json()[
        "items"
    ]
    # print(album_items)
    if album_items[0] != None and len(album_items) != 0:
        album_ids = [
            album["album"].get("id")
            for album in album_items
            if album and album.get("album", None)
        ]
        requests_wrapper.delete(
            f'https://api.spotify.com/v1/me/albums?ids={",".join(album_ids)}'
        )

    # remove all following artists
    artist_items = json.loads(
        requests_wrapper.get("https://api.spotify.com/v1/me/following?type=artist").text
    )["artists"]["items"]
    if len(artist_items) != 0:
        artist_ids = [artist["id"] for artist in artist_items]
        requests_wrapper.delete(
            f'https://api.spotify.com/v1/me/following?type=artist&ids={",".join(artist_ids)}'
        )

    # add top-3 tracks of Lana Del Rey, Whitney Houston to my music, DONE
    artist_id_1 = requests_wrapper.get(
        f"https://api.spotify.com/v1/search?q=Lana%20Del%20Rey&type=artist"
    )
    artist_id_1 = json.loads(artist_id_1.text)["artists"]["items"][0]["id"]
    track_ids_1 = requests_wrapper.get(
        f"https://api.spotify.com/v1/artists/{artist_id_1}/top-tracks?country=US"
    )
    track_ids_1 = json.loads(track_ids_1.text)["tracks"]
    track_ids_1 = [track["id"] for track in track_ids_1][:3]
    requests_wrapper.put(
        f'https://api.spotify.com/v1/me/tracks?ids={",".join(track_ids_1)}', data=None
    )

    artist_id_2 = requests_wrapper.get(
        f"https://api.spotify.com/v1/search?q=Whitney%20Houston&type=artist"
    )
    artist_id_2 = json.loads(artist_id_2.text)["artists"]["items"][0]["id"]
    track_ids_2 = requests_wrapper.get(
        f"https://api.spotify.com/v1/artists/{artist_id_2}/top-tracks?country=US"
    )
    track_ids_2 = json.loads(track_ids_2.text)["tracks"]
    track_ids_2 = [track["id"] for track in track_ids_2][:3]
    requests_wrapper.put(
        f'https://api.spotify.com/v1/me/tracks?ids={",".join(track_ids_2)}', data=None
    )

    # search for the top-3 tracks of The Beatles
    artist_id_3 = requests_wrapper.get(
        f"https://api.spotify.com/v1/search?q=The%20Beatles&type=artist"
    )
    artist_id_3 = json.loads(artist_id_3.text)["artists"]["items"][0]["id"]
    track_ids_3 = requests_wrapper.get(
        f"https://api.spotify.com/v1/artists/{artist_id_3}/top-tracks?country=US"
    )
    track_ids_3 = json.loads(track_ids_3.text)["tracks"]
    track_ids_3 = [track["id"] for track in track_ids_3][:3]

    # follow Lana Del Rey, Whitney Houston, The Beatles, DONE
    requests_wrapper.put(
        f'https://api.spotify.com/v1/me/following?type=artist&ids={",".join([artist_id_1, artist_id_2, artist_id_3])}',
        data=None,
    )

    # create playlist My R&B, My Rock. Add top-3 tracks of Whitney Houston to My R&B, top-3 tracks of The Beatles to My Rock, DONE
    playlist_id_1 = requests_wrapper.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists", data={"name": "My R&B"}
    )
    playlist_id_1 = json.loads(playlist_id_1.text)["id"]
    requests_wrapper.post(
        f'https://api.spotify.com/v1/playlists/{playlist_id_1}/tracks?uris={",".join([f"spotify:track:{track_id}" for track_id in track_ids_2])}',
        data=None,
    )

    playlist_id_2 = requests_wrapper.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        data={"name": "My Rock"},
    )
    playlist_id_2 = json.loads(playlist_id_2.text)["id"]
    requests_wrapper.post(
        f'https://api.spotify.com/v1/playlists/{playlist_id_2}/tracks?uris={",".join([f"spotify:track:{track_id}" for track_id in track_ids_3])}',
        data=None,
    )

    # add Born To Die and reputation to my album. play Lana Del Rey's album "Born To Die"
    album_id_1 = requests_wrapper.get(
        f"https://api.spotify.com/v1/search?q=Born%20To%20Die&type=album"
    )
    album_id_1_id = json.loads(album_id_1.text)["albums"]["items"][0]["id"]
    album_id_1_uri = json.loads(album_id_1.text)["albums"]["items"][0]["uri"]
    requests_wrapper.put(
        "https://api.spotify.com/v1/me/albums", data={"ids": [album_id_1_id]}
    )
    res = requests_wrapper.put(
        f"https://api.spotify.com/v1/me/player/play",
        data={"context_uri": album_id_1_uri},
    )
    # print(res)

    album_id_2 = requests_wrapper.get(
        f"https://api.spotify.com/v1/search?q=reputation&type=album"
    )
    album_id_2 = json.loads(album_id_2.text)["albums"]["items"][0]["id"]
    requests_wrapper.put(
        f"https://api.spotify.com/v1/me/albums?ids={album_id_2}", data=None
    )
