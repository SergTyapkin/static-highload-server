class HttpParser:
    def __init__(self):
        self.method = None
        self.path = None
        self.query = None
        self.http_version = None
        self.headers = {}
        self.is_path_complete = False
        self.is_headers_complete = False
        self.is_message_complete = False
        self.is_found_error = False
        self.bytes = b""
        self._last_string = ""

    def execute(self, chunk: bytes):
        if self.is_found_error:
            return

        self.bytes += chunk
        chunk_str = chunk.decode()
        if self.bytes.endswith(b"\r\n\r\n"):
            if self.is_headers_complete:
                self.is_message_complete = True
            else:
                self.is_headers_complete = True

        new_strings = (self._last_string + chunk_str).split('\r\n')
        completed_new_strings = new_strings[:-1]
        self._last_string = new_strings[-1]

        for string in completed_new_strings:
            if string == "":
                continue

            if not self.is_path_complete:
                words = string.split(' ')
                if len(words) != 3:
                    self.is_found_error = True
                    return

                self.method = words[0]

                path_and_query = words[1].split('?')
                if len(path_and_query) > 2:
                    self.is_found_error = True
                    return
                if len(path_and_query) == 2:
                    self.path = path_and_query[0]
                    self.query = path_and_query[1]
                else:
                    self.path = words[1]

                self.http_version = words[2]
                self.is_path_complete = True
                continue

            words = string.split(': ')
            if len(words) != 2:
                self.is_found_error = True
                return
            self.headers[words[0]] = words[1]
