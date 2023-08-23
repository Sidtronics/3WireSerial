import code
import serial
from enum import Enum

# Change port here.
PORT = '/dev/ttyACM0'

# Command characters.
class Command(Enum):
    SEND = 'S'
    READ = 'R'
    STB_HIGH = 'H'
    STB_LOW = 'L'

# defs for stb().
HIGH = True;
LOW = False;

class SerialDevice :

    def __init__(self, port) :

        self.ser = serial.Serial()
        self.ser.port = port

        print("Waiting for device at port:", self.ser.name)
        while True:

            try:
                self.ser.open()
            except serial.SerialException:
                pass
            else:
                print("Port opened at:", self.ser.name)
                print("-" * 40)
                break

    def send(self, *data:int, count:int=1) :

        self.ser.write(Command.SEND.value.encode())
        self.ser.write((len(data)*count).to_bytes(1))

        for _ in range(count) :
            self.ser.write(bytes(data))

        ack = self.ser.read()
        print(f"\n{int.from_bytes(ack)} Bytes sent.\n")

    def send_str(self, string:str) :

        self.ser.write(Command.SEND.value.encode())
        self.ser.write(len(string).to_bytes(1))
        self.ser.write(string.encode())

        ack = self.ser.read()
        print(f"\n{int.from_bytes(ack)} Characters sent.\n")

    def recv(self, count:int=1) :
        
        self.ser.write(Command.READ.value.encode())
        self.ser.write(count.to_bytes(1))
        
        print("\n     HEX  BIN        DEC")
        for n in range(count) :
            byte = self.ser.read()
            print("[{0:02d}] {1:02X} : {1:08b} : {1:03d}".format(n+1, int.from_bytes(byte)))

        print(f"\n{count} Bytes received.\n")

    def stb(self, sig:bool) :

        if sig == True :
            cmd = Command.STB_HIGH

        else :
            cmd = Command.STB_LOW

        self.ser.write(cmd.value.encode())
        self.ser.read()
        print("\nStrobe pin held {}.\n".format(cmd.name[4:]))

if __name__ == "__main__":

    dbg = SerialDevice(PORT)
    code.interact(local=locals(),banner="")

