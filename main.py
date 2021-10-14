from server import run_server

from utils import read_config

if __name__ == '__main__':
    run_server(read_config("config.json"))
