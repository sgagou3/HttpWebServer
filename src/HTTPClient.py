import os
import socket
import sys


def main():
    # Preset the hostname as the hostname
    # of the current machine and read in
    # the port number from the command line
    port_number = sys.argv[1]

    request = sys.stdin.readlines()
    # Wait for and process user input
    for line in request:
        # Socket creation
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(9.9)
        try:
            client_socket.connect(("", int(port_number)))
            # Process and validate input
            client_socket.send(line.encode())
            result = client_socket.recv(2048).decode()
            # Close the socket
            client_socket.close()

            # Print output
            print(line, end="")
            print(result, end="")
        except:
            print("Connection Error")
            client_socket.close()


if __name__ == '__main__':
    main()
