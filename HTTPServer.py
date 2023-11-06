__author__ = "730474971"

import errno
import sys
import os
import socket

OK = -1
BAD_METHOD = 0
BAD_REQUEST = 1
BAD_VERSION = 2
EXTRA_TOKEN = 3


# Processes method token and returns
# error code back to the "process"
# function.
def process_method_token(token):
    if token != "GET":
        return BAD_METHOD
    return OK


# Processes absolute path token
# and returns error code back to
# process function.
def process_request_token(token):
    # Ensure the token even exists
    if len(token) > 0:
        # Grammar check
        if token[0] != "/":
            return BAD_REQUEST
        for char in token:
            if (
                    # Character check
                    not 48 <= ord(char) <= 57
                    and not 65 <= ord(char) <= 90
                    and not 97 <= ord(char) <= 122
                    and ord(char) != 46
                    and ord(char) != 47
                    and ord(char) != 95
            ):
                return BAD_REQUEST
    else:
        return BAD_REQUEST
    return OK


# Processes the version toke and returns
# error code back to "process"
# function
def process_version_token(token):
    t = token.split("/")
    # Make sure we have correct request format
    if len(t) != 2:
        return BAD_VERSION
    elif t[0] != "HTTP" or len(t[1]) < 3:
        return BAD_VERSION
    # Make sure we have exactly two lines of digits
    elif len(t[1].split(".")) != 2:
        return BAD_VERSION
    # Grammar check
    elif not "".join(t[1].split(".")).isnumeric():
        return BAD_VERSION
    return OK


# Splits up processing the request line
# into three different sub-problems
# and prints out what is needed.
def process(request):
    match len(request):
        # Each case represents how many visible tokens there
        # are of the entire request, done through splitting
        # the original request string.
        case 0:
            return "ERROR -- Invalid Method token.\r"
        case 1:
            if process_method_token(request[0]) != OK:
                return "ERROR -- Invalid Method token.\r"
            else:
                return "ERROR -- Invalid Absolute-Path token.\r"
        case 2:
            if process_method_token(request[0]) != OK:
                return "ERROR -- Invalid Method token.\r"
            elif process_request_token(request[1]) != OK:
                return "ERROR -- Invalid Absolute-Path token.\r"
            else:
                return "ERROR -- Invalid HTTP-Version token.\r"
        case 3:
            if process_method_token(request[0]) != OK:
                return "ERROR -- Invalid Method token.\r"
            elif process_request_token(request[1]) != OK:
                return "ERROR -- Invalid Absolute-Path token.\r"
            elif process_version_token(request[2]) != OK:
                return "ERROR -- Invalid HTTP-Version token.\r"
            else:
                return print_valid_request(request)
        case _:
            if process_method_token(request[0]) != OK:
                return "ERROR -- Invalid Method token.\r"
            elif process_request_token(request[1]) != OK:
                return "ERROR -- Invalid Absolute-Path token.\r"
            elif process_version_token(request[2]) != OK:
                return "ERROR -- Invalid HTTP-Version token.\r"
            else:
                return "ERROR -- Spurious token before CRLF.\r"


# If the request from "process" function
# is valid, the request is printed out here
# unless the file cannot be found.
def print_valid_request(request):
    result = ""
    result += ("Method = " + request[0] + "\r")
    result += ("Request-URL = " + request[1] + "\r")
    result += ("HTTP-Version = " + request[2] + "\r")
    # Case insensitive file extensions
    if (
            not request[1].lower().endswith(".htm")
            and not request[1].lower().endswith(".html")
            and not request[1].lower().endswith(".txt")
    ):
        result += ("501 Not Implemented: " + request[1] + "\r")
    else:
        # Ensure we can read the file at the end of the
        # absolute path
        if not os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + "/" + request[1][1:]):
            result += ("404 Not Found: " + request[1] + "\r")
        else:
            try:
                with open(os.path.dirname(os.path.abspath(__file__)) + "/" + request[1][1:], "r") as f:
                    result += (f.read().rstrip() + "\r")
            except Exception as e:
                result += ("ERROR: " + str(e) + "\r")
    return result


def main():
    # Read in the port number
    # and ensure it is an integer
    port_num = sys.argv[1]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(("", int(port_num)))
        server_socket.listen(1)
        server_socket.settimeout(9.9)
    except:
        print("Connection Error")
        server_socket.close()
        return

    while True:
        try:
            # Listen for a single client connection
            connection, address = server_socket.accept()
            print("Client Connected to COMP431 HTTP Server")
            # Read in each of the lines and handle each
            # as a separate request.
            if connection:
                request = connection.recv(2048).decode()
                result = process(request.split())

                connection.send(result.encode())
                connection.close()
            else:
                print("Connection Error")
        except:
            print("Connection Error")
            server_socket.close()
            break


if __name__ == "__main__":
    main()
