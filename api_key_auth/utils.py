from rest_framework.request import Request

def get_api_key(request: Request, api_key_header, key_in_query_params) -> str:
    """
    Retrieve the API key from the request.

    Args:
        request: The incoming HTTP request.
        api_key_header (str): The HTTP header used to pass the API key.
        key_in_query_params (bool): Flag to indicate if the key can also be passed in query params.

    Returns:
        str: The API key if present, None otherwise.

    Raises:
        ValueError: If the api_key_header is not properly set or the API key is not found.
    """
    if not api_key_header:
        raise ValueError("api_key_header is not set.")

    key = request.query_params.get(api_key_header) if key_in_query_params else None
    key = key or request.META.get(api_key_header)

    if not key:
        raise ValueError("API key not found in the request headers or query parameters.")
    
    return key
