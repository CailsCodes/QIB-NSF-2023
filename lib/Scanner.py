import serial

class Scanner:

    def __init__(self, _port):
        self._port = _port
        self.conn = self.connect_scanner(_port)

    def connect_scanner(self, port):
        return serial.Serial(port)

    def close_connection(self):
        self._input.close()

    def is_connected(self):
        port_found = (self._port in get_ports())
        return True if port_found else False

    def maintain_connection(self):
        "DO NOT RUN IN MAIN LOOP"
        CHECK_FREQUENCY = 5 #seconds
        self.conn = self.connect_scanner(self._port)
        while self.is_connected():
            time.sleep(CHECK_FREQUENCY)
        self.maintain_connection()