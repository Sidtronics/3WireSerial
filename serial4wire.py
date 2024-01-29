import code
import serial
from enum import Enum

# Change port here.
PORT = "/dev/ttyACM0"


# Command characters.
class Command(Enum):
    SEND = "S"
    READ = "R"
    STB_HIGH = "H"
    STB_LOW = "L"


class SerialDevice:
    def __init__(self, port):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = 9600

        print("[4WireSerial] Waiting for device at port:", self.ser.name)
        while True:
            try:
                self.ser.open()
            except serial.SerialException:
                pass
            else:
                print("[4WireSerial] Port opened at:", self.ser.name)
                print("[4WireSerial] Waiting for ready signal...")
                break

        self.ser.read()  # wait for ready signal
        print("[4WireSerial] Device ready!")

    # Low level methods:

    def send(self, *data: int):
        self.ser.write(Command.SEND.value.encode())
        self.ser.write(len(data).to_bytes(1))
        self.ser.write(bytes(data))

        sent_bytes = self.ser.read()
        return int.from_bytes(sent_bytes)

    def recv(self, count: int = 1):
        self.ser.write(Command.READ.value.encode())
        self.ser.write(count.to_bytes(1))

        received_bytes = list(self.ser.read(count))
        return received_bytes

    def stb(self, val: bool):
        cmd = Command.STB_HIGH if val else Command.STB_LOW

        self.ser.write(cmd.value.encode())
        self.ser.read()  # ACK

    # Other convenient methods:

    def send_str(self, string: str):
        sent_bytes = self.send(*tuple(map(ord, string)))
        return sent_bytes

    def send_cmd(self, cmd: int, *data: int):
        self.stb(False)
        sent_bytes = self.send(cmd)

        if data != ():
            sent_bytes += self.send(*data)

        self.stb(True)
        return sent_bytes

    def recv_data(self, cmd: int, count: int = 1):
        self.stb(False)
        self.send(cmd)
        received_bytes = self.recv(count)
        self.stb(True)

        return received_bytes


if __name__ == "__main__":
    dbg = SerialDevice(PORT)

    # Wrapper functions for verbosity and convenience in interactive mode:

    def send(*data: int):
        print("\n     HEX  BIN        DEC")
        for n in range(len(data)):
            print("[{0:02d}] {1:02X} : {1:08b} : {1:03d}".format(n + 1, data[n]))

        sent = dbg.send(*data)
        print(f"\n{sent} Byte(s) sent.\n")

    def recv(count: int = 1):
        print("\n     HEX  BIN        DEC")

        received = dbg.recv(count)
        for n in range(count):
            print("[{0:02d}] {1:02X} : {1:08b} : {1:03d}".format(n + 1, received[n]))

        print(f"\n{count} Byte(s) received.\n")

    def stb(val: bool):
        dbg.stb(val)
        print("\nStrobe pin held {}.\n".format("HIGH" if val else "LOW"))

    def send_str(string: str):
        print("\n     HEX  BIN        DEC   ASCII")
        for n in range(len(string)):
            print(
                "[{0:02d}] {1:02X} : {1:08b} : {1:03d} : {1:c}".format(
                    n + 1, ord(string[n])
                )
            )

        sent = dbg.send_str(string)
        print(f"\n{sent} Character(s) sent.\n")

    def send_cmd(cmd: int, *data: int):
        print("\n      HEX  BIN        DEC")
        print("[CMD] {0:02X} : {0:08b} : {0:03d}".format(cmd))
        for n in range(len(data)):
            print("[{0:03d}] {1:02X} : {1:08b} : {1:03d}".format(n + 1, data[n]))

        sent = dbg.send_cmd(cmd, *data)
        print(f"\n{sent} Byte(s) sent.\n")

    def recv_data(cmd: int, count: int = 1):
        print("\n     HEX  BIN        DEC")

        received = dbg.recv_data(cmd, count)
        for n in range(count):
            print("[{0:02d}] {1:02X} : {1:08b} : {1:03d}".format(n + 1, received[n]))

        print(f"\n{count} Byte(s) received.\n")

    # Start interactive console.
    print("[4WireSerial] Starting interactive console:\n")
    code.interact(local=locals(), banner="")
