import time
from urllib.parse import unquote
import socket
import os

from utils import receive_data
from HttpParser import HttpParser 


ALLOWED_METHODS = ['HEAD', 'GET']

STATUS_OK = '200 OK'
STATUS_BAD_REQUEST = '400 Bad Request'
STATUS_FORBIDDEN = '403 Forbidden'
STATUS_NOT_FOUND = '404 Not Found'
STATUS_METHOD_NOT_ALLOWED = '405 Method Not Allowed'

CONTENT_TYPE = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'text/javascript',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'swf': 'application/x-shockwave-flash'
}


def response(sock: socket, status: str, server_name: str = '', path: str = '', method: str = ''):
    body = b''
    content_length = 0
    last_modified = ''
    if status == STATUS_OK:
        with open(path, 'rb') as file:
            body = file.read()
            content_length = len(body)
            body += b"\r\n\r\n"
            last_modified = time.ctime(os.path.getmtime(path))
    if method == 'HEAD':
        body = b''

    headers = (f"HTTP/1.1 {status}\r\n") + \
              (f"Server: {server_name}\r\n" if server_name else '') + \
              (f"Content-Type: {CONTENT_TYPE.get(path.split('.')[-1])}\r\n" if path else '') + \
              (f"Content-Length: {content_length}\r\n" if content_length else '') + \
              (f"Connection: close\r\n") + \
              (f"Last-Modified: {last_modified}\r\n" if last_modified else '') + \
              (f"Date: {time.strftime('%c')}\r\n\r\n")

    sock.sendall(headers.encode() + body)
    sock.close()


def handle(sock: socket, config: dict):
    parser = HttpParser()
    receive_data(sock, parser)

    method = parser.method
    parser_path = parser.path
    server_name = config['name']
    static_dir = config['directory']
    url_prefix = config['url_prefix']

    if (not parser.is_headers_complete) or (not parser_path):
        response(sock, STATUS_BAD_REQUEST, server_name)
        return

    try:
        parser_path = unquote(parser_path)
    except TypeError:
        pass

    if not parser_path.startswith(url_prefix):
        response(sock, STATUS_NOT_FOUND, server_name)
        return
    path = static_dir + parser_path[len(url_prefix):]
    if method not in ALLOWED_METHODS:
        response(sock, STATUS_METHOD_NOT_ALLOWED, server_name)
        return
    if parser_path.find('../') != -1:
        response(sock, STATUS_FORBIDDEN, server_name)
        return
    it_was_dir = False
    if (path[-1] == '/') and os.path.isdir(path):
        path += 'index.html'
        it_was_dir = True
    if not os.path.isfile(path):
        if it_was_dir:
            response(sock, STATUS_FORBIDDEN, server_name)
            return
        response(sock, STATUS_NOT_FOUND, server_name)
        return

    response(sock, STATUS_OK, server_name, path, method)
