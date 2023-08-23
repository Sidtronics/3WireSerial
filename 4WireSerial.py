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

# defs for set_stb().
HIGH = True;
LOW = False;

class SerialDevice :

    def __init__(self, port) :

        self.ser = serial.Serial()
        self.ser.port = port

        print("[4WireSerial] Waiting for device at port:", self.ser.name)
        while True:

            try:
                self.ser.open()
            except serial.SerialException:
                pass
            else:
                print("[4WireSerial] Port opened at:", self.ser.name)
                break

    def send(self, *data:int, count:int=1) :

        self.ser.write(Command.SEND.value.encode())
        self.ser.write((len(data)*count).to_bytes(1))

        for _ in range(count) :
            self.ser.write(bytes(data))

        sent_bytes = self.ser.read()
        return int.from_bytes(sent_bytes)

        
    def send_str(self, string:str) :

        self.ser.write(Command.SEND.value.encode())
        self.ser.write(len(string).to_bytes(1))
        self.ser.write(string.encode())

        sent_bytes = self.ser.read()
        return int.from_bytes(sent_bytes)

        
    def recv(self, count:int=1) :
        
        self.ser.write(Command.READ.value.encode())
        self.ser.write(count.to_bytes(1))
        
        received_bytes = list(self.ser.read(count))
                
        return received_bytes
        
    def set_stb(self, val:bool) :

        cmd = Command.STB_HIGH if val else Command.STB_LOW

        self.ser.write(cmd.value.encode())
        self.ser.read() # ACK
        
if __name__ == "__main__":


    dbg = SerialDevice(PORT)

    def send(*data:int, count:int=1) :

        print("\n     HEX  BIN        DEC")
        for n in range(count*len(data)) :
            print("[{0:02d}] {1:02X} : {1:08b} : {1:03d}".format(n+1, data[n % len(data)]))

        sent = dbg.send(*data, count=count)
        print(f"\n{sent} Byte(s) sent.\n")

    def send_str(string:str) :
        
        print("\n     HEX  BIN        DEC   ASCII")
        for n in range(len(string)) :
            print("[{0:02d}] {1:02X} : {1:08b} : {1:03d} : {1:c}".format(n+1, ord(string[n])))

        sent = dbg.send_str(string)
        print(f"\n{sent} Character(s) sent.\n")

    def recv(count:int=1) :

        print("\n     HEX  BIN        DEC")

        received = dbg.recv(count)
        for n in range(count) :
            print("[{0:02d}] {1:02X} : {1:08b} : {1:03d}".format(n+1, received[n]))

        print(f"\n{count} Byte(s) received.\n")

    def set_stb(val:bool) :

        dbg.set_stb(val)
        print("\nStrobe pin held {}.\n".format("HIGH" if val else "LOW"))

    # Start interactive console.
    print("[4WireSerial] Starting interactive console:\n")
    code.interact(local=locals(),banner="")

