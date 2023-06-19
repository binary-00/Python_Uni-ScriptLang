import pytest


class HttpRequest:
    def __init__(self, request_type, resource_path, http_protocol):
        self.request_type = request_type
        self.resource_path = resource_path
        self.http_protocol = http_protocol


class BadRequestTypeError(Exception):
    pass


class BadHTTPVersion(Exception):
    pass


def reqstr2obj(request_string):
    # Check if the argument is a string
    if not isinstance(request_string, str):
        raise TypeError("Argument must be a string")

    # Split the request string into its components
    request_components = request_string.split()

    # Check if the request string consists of three words separated by a single space
    if len(request_components) != 3:
        return None

    # Check if the request type is valid
    valid_request_types = ["GET", "POST", "PUT", "DELETE"]
    if request_components[0] not in valid_request_types:
        raise BadRequestTypeError(f"Invalid request type: {request_components[0]}")
    
    """
    # Check if the HTTP version is valid
    # (9. removing this block will not raise a BadHttpVer. error & t7=f.)
    valid_http_versions = ["HTTP1.0", "HTTP1.1", "HTTP2.0"]
    if request_components[2] not in valid_http_versions:
        raise BadHTTPVersion(f"Invalid HTTP version: {request_components[2]}")

    # Check if the resource path starts with a slash
    # (10. removing these lines will not raise a ValueError & t10=f.)
    if not request_components[1].startswith("/"):
        raise ValueError("Path must start with /")
    """
    
    # Create an HttpRequest object with the components
    request = HttpRequest(
        request_components[0], request_components[1], request_components[2]
    )
    request = HttpRequest("POST", "/", "HTTP1.1") #(5. will fail because of wrong request type)
    #return request


def test_reqstr2obj_type_error():
    # function raises a TypeError when called with a non-string argument
    with pytest.raises(TypeError):
        reqstr2obj(abc)


def test_reqstr2obj_return_object():
    # Test if the function returns an object of an HTTP request class if called with an argument: "GET / HTTP1.1”
    result = reqstr2obj("GET / HTTP1.1")
    assert isinstance(result, HttpRequest)
    assert result.request_type == "GET"
    assert result.resource_path == "/"
    assert result.http_protocol == "HTTP1.1"


def test_reqstr2obj_return_object_attributes():
    # Test if the function returns an object of an HTTP request class with attributes set correctly
    result = reqstr2obj("GET / HTTP1.1")
    assert isinstance(result, HttpRequest)
    assert result.request_type == "GET"
    assert result.resource_path == "/"
    assert result.http_protocol == "HTTP1.1"


def test_reqstr2obj_return_relevant_object():
    # Test if the function returns an object relevant to the argument
    result = reqstr2obj("POST /test HTTP1.0")
    assert isinstance(result, HttpRequest)
    assert result.request_type == "POST"
    assert result.resource_path == "/test"
    assert result.http_protocol == "HTTP1.0"


def test_reqstr2obj_return_none():
    # Test if the function returns None if a request string does not consist of three words separated by a single space
    result = reqstr2obj("GET /")
    #assert result is None
    assert result is not None #(7. fails, is not = not None)


def test_reqstr2obj_bad_request_type_error():
    # Test if the function raises exception BadRequestTypeError if called with string that uses illegal request type (e.g. "DOWNLOAD /movie.mp4 HTTP1.1”)
    with pytest.raises(BadRequestTypeError):
        reqstr2obj("DOWNLOAD /movie.mp4 HTTP1.1")
    result = reqstr2obj("DOWNLOAD /movie.mp4 HTTP1.1") #(8. illegal req type)


def test_reqstr2obj_bad_http_version_error():
    # Test if the function raises exception BadHTTPVersion if called with string that contains string other then: HTTP1.0, HTTP1.1 or HTTP2.0
    with pytest.raises(BadHTTPVersion):
        reqstr2obj("GET / HTTP3.0")


def test_reqstr2obj_value_error():
    # Test if the function raises exception ValueError, containing a text “Path must start with /” if the path does not start with the slash (“/”) character
    with pytest.raises(ValueError) as excinfo:
        reqstr2obj("GET test HTTP1.1")
    assert str(excinfo.value) == "Path must start with /"


if __name__ == "__main__":
    try:
        # Run the first test
        test_reqstr2obj_type_error()
        print("Test 1 passed!")
    except:
        print("Test 1 failed!")

    try:
        # Run the second test
        test_reqstr2obj_return_object()
        print("Test 2 passed!")
    except:
        print("Test 2 failed!")

    try:
        # Run the third test
        test_reqstr2obj_return_object_attributes()
        print("Test 3 passed!")
    except:
        print("Test 3 failed!")

    try:
        # Run the fourth test
        test_reqstr2obj_return_relevant_object()
        print("Test 4 passed!")
    except:
        print("Test 4 failed!")

    try:
        # Run the fifth test
        test_reqstr2obj_return_none()
        print("Test 5 passed!")
    except:
        print("Test 5 failed!")

    try:
        # Run the sixth test
        test_reqstr2obj_bad_request_type_error()
        print("Test 6 passed!")
    except:
        print("Test 6 failed!")

    try:
        # Run the seventh test
        test_reqstr2obj_bad_http_version_error()
        print("Test 7 passed!")
    except:
        print("Test 7 failed!")

    try:
        # Run the eighth test
        test_reqstr2obj_value_error()
        print("Test 8 passed!")
    except:
        print("Test 8 failed!")
