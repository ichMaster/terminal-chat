"""Synchronous single-client TCP echo server."""

import socket

HOST = "127.0.0.1"
PORT = 9000
BUFFER_SIZE = 1024


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(1)
        print(f"Echo server listening on {HOST}:{PORT}")

        while True:
            conn, addr = srv.accept()
            print(f"[+] Client connected: {addr[0]}:{addr[1]}")
            try:
                with conn:
                    while True:
                        data = conn.recv(BUFFER_SIZE)
                        if not data:
                            break
                        conn.sendall(data)
            except ConnectionResetError:
                print(f"[!] Client {addr[0]}:{addr[1]} disconnected abruptly")
            finally:
                print(f"[-] Client disconnected: {addr[0]}:{addr[1]}")


if __name__ == "__main__":
    main()
