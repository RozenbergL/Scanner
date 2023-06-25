import socket
import threading
import argparse
from queue import Queue


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='IP address to scan')
    parser.add_argument('start_port', type=int, help='Start scanning port')
    parser.add_argument('finish_port', type=int, help='Finish scanning port')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads')

    return parser.parse_args()


def main(ip, start_port, finish_port, threads_count):
    queue = Queue()
    for port in range(start_port, finish_port + 1):
        queue.put(port)

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=helper, args=(queue, ip))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def helper(queue, ip):
    while not queue.empty():
        port = queue.get()
        if tcp_scaner(ip, port):
            print(f'TCP port {port} open')
        if udp_scaner(ip, port):
            print(f'UDP port {port} open')


def tcp_scaner(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip, port))
        return True
    except:
        return False
    finally:
        sock.close()


def udp_scaner(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)

    try:
        sock.sendto(b'test', (ip, port))
        sock.recvfrom(1024)
        return True
    except socket.timeout:
        return False
    except:
        return True
    finally:
        sock.close()


if __name__ == '__main__':
    arguments = parse()
    main(arguments.ip, arguments.start_port, arguments.finish_port, arguments.threads)
