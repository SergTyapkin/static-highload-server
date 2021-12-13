import threading
import multiprocessing
import socket
from handler import handle


def listen_forever(sock, config):
    while True:
        conn, address = sock.accept()  # waiting for connection
        handle(conn, config)
        conn.close()


def run_process(sock, config):
    threads = []
    for _ in range(config['threads_limit']):
        thread = threading.Thread(target=listen_forever, args=(sock, config))
        thread.start()
        threads += [thread]

    for thread in threads:
        thread.join()


def run_server(config):
    process_limit = config['process_limit']
    if process_limit > 0:
        process_limit = min(process_limit, multiprocessing.cpu_count())
    else:
        process_limit = multiprocessing.cpu_count()

    if process_limit > 1:
        try:
            multiprocessing.set_start_method('fork')
        except ValueError:
            print("This program can't works in your OS. Need POSIX-system.")
            return
        print("Number of processes:", process_limit)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((config['host'], config['port']))
    sock.listen(config['connections_limit'])
    print("Server listening on port", config['port'])

    processes = []
    for i in range(1, process_limit + 1):
        process = multiprocessing.Process(target=run_process, args=(sock, config))
        process.start()
        print("Process #", process.pid, " started", sep="")
        processes += [process]

    for process in processes:
        process.join()
