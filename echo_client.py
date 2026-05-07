"""Synchronous TCP echo client — sends stdin lines, prints echoed response."""

import socket

HOST = "127.0.0.1"
PORT = 9000
BUFFER_SIZE = 1024


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}. Type lines to echo (Ctrl+D to quit).")

        try:
            while True:
                line = input("> ")
                if not line:
                    continue
                sock.sendall((line + "\n").encode())
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    print("Server closed connection.")
                    break
                print(f"< {data.decode()}", end="")
        except (EOFError, KeyboardInterrupt):
            print("\nDisconnecting.")


if __name__ == "__main__":
    main()
