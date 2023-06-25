import socket
import threading


def test_tcp_server(host, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host, port))
    server_sock.listen()
    print(f"Server running {host}:{port}")

    while True:
        client_sock, address = server_sock.accept()
        client_sock.recv(1024)
        client_sock.close()


if __name__ == '__main__':
    t = threading.Thread(target=test_tcp_server, args=('127.0.0.1', 1101))
    t.start()
    t.join()
