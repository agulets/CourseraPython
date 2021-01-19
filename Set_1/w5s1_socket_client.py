import socket
import time


class ClientError(Exception):
    def __init__(self, text):
        self.text = text
        if text:
            print(f"Error: '{self.text}'")
    pass


class Client:
    def __init__(self, address, port, timeout=None):
        self._address = address
        self._port = int(port)
        self._timeout = int(timeout)

    @staticmethod
    def check_response_status(response):
        if response[0:3] != 'ok\n':
            raise ClientError(str(response))

    @staticmethod
    def check_timestamp(timestamp):
        try:
            return int(timestamp)
        except Exception:
            return None

    @staticmethod
    def check_response_in_get(response):
        for line in response.split('\n')[1:-2]:
            data = line.split(' ')

            if len(data) != 3:
                raise ClientError('Len != 3')

            try:
                float(data[1])
                int(data[2])
            except ValueError:
                raise ClientError('Value error ')

    def connection(self, request):
        with socket.create_connection((self._address, self._port), self._timeout) as sock:
            sock.sendall(request.encode("utf8"))
            response = sock.recv(1024).decode('utf-8')
            self.check_response_status(response)
            return response

    def get(self, key):
        get_command = f"get {key}\n"
        response = self.connection(get_command)
        self.check_response_in_get(response)
        decoded_data = dict()
        lines = response.split('\n')

        for line in lines[1:-2]:
            line_data = line.split(' ')
            key = line_data[0]
            value = float(line_data[1])
            timestamp = int(line_data[2])
            if key not in decoded_data.keys():
                decoded_data[key] = list()
            decoded_data[key].append((timestamp, value))

        for key in decoded_data.keys():
            decoded_data[key].sort(key=lambda tup: tup[0])

        return decoded_data

    def put(self, key, val, timestamp=None):
        timestamp = self.check_timestamp(timestamp) if timestamp else int(time.time())
        put_command = f"put {key} {val} {timestamp}\n"
        self.connection(put_command)

