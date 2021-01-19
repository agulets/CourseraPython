import asyncio

STORAGE = dict()


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        response = self.process(data.decode('utf-8').strip('\r\n')).encode('utf-8')
        self.transport.write(response)

    @staticmethod
    def check_timestamp(timestamp):
        try:
            int(timestamp)
        except ValueError:
            return False
        return True

    @staticmethod
    def check_data(data):
        try:
            float(data)
        except ValueError:
            return False
        return True

    @staticmethod
    def get(key):
        response = 'ok\n'
        if key == '*':
            for key, values in STORAGE.items():
                for value in values:
                    response = f"{response}{key} {value[1]} {value[0]}\n"
        else:
            if key in STORAGE:
                for value in STORAGE[key]:
                    response = f"{response}{key} {value[1]} {value[0]}\n"

        return f"{response}\n"

    @staticmethod
    def put(key, value, timestamp):
        if key == '*':
            return f"error\nkey cannot contain *\n\n"

        if key not in STORAGE:
            STORAGE[key] = list()
            STORAGE[key].append((timestamp, float(value)))
        else:
            for element in STORAGE[key]:
                s_timestamp, s_value = element
                if s_timestamp == timestamp:
                    STORAGE[key].remove(element)
            STORAGE[key].append((timestamp, float(value)))

        STORAGE[key].sort(key=lambda tup: tup[0])
        return 'ok\n\n'

    def process(self, request):
        response = f"error\nwrong command\n\n"
        request_parts = request.split(' ')
        # print(len())
        # print

        if len(request_parts) >= 2:
            if request_parts[0] == 'get':
                if request_parts[1] and len(request_parts) == 2:
                    response = self.get(request_parts[1])
            if request_parts[0] == 'put':
                if len(request_parts) == 4 and request_parts[1] and request_parts[2] and request_parts[3] \
                        and self.check_timestamp(request_parts[3]) and self.check_data(request_parts[2]):
                    response = self.put(request_parts[1], request_parts[2], request_parts[3])
        return response


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coroutine)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8181)

