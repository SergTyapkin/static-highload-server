import socket
import json
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser


RECV_TIMEOUT = 20
BUF_SIZE = 4096


def receive_data(sock: socket, parser: HttpParser) -> bytes:
    data = b""
    sock.settimeout(RECV_TIMEOUT)
    while not parser.is_headers_complete():
        try:
            chunk = sock.recv(BUF_SIZE)
        except:
            break
        if not chunk:
            break

        parser.execute(chunk, len(chunk))
        data += chunk
        if data.decode().endswith('\n'):
            break
    return data


def read_config(filepath: str) -> dict:
    try:
        file = open(filepath, "r")
        config = json.load(file)
        file.close()
        config["proxy_host"] = ""
        return config
    except:
        print("Can't open and serialize config.json")
        exit()
