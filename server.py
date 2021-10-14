import threading
import socket
from handler import handle


def listen_forever(sock, config):
    while True:
        conn, address = sock.accept()  # waiting for connection
        handle(conn, config)
        conn.close()


def run_server(config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((config['host'], config['port']))
    sock.listen(config['connections_limit'])

    print("Server listening on port", config['port'])
    threads = []
    for _ in range(config['forks_limit']):
        thread = threading.Thread(target=listen_forever, args=(sock, config))
        thread.start()

        threads += [thread]

    for thread in threads:
        thread.join()
