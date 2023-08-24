# 4WireSerial
Simple tool to communicate with 4-wire serial interface devices through Arduino. Also supports 3-wire serial interface.

Supports devices with following pinouts:
+ 4-wire serial interface (strobe, clock, data_in, data_out)
+ 3-wire serial interface (strobe, clock, data_in/out)

## Requirements
python >= 3.6

## Installation

### Download
```
$ git clone https://github.com/Sidtronics/4WireSerial.git
```
or download [zip](https://github.com/Sidtronics/4WireSerial/archive/refs/heads/main.zip).

### Install Dependencies
```
$ pip install -r requirements.txt
```
## Configuration

### Change port
If using interactive mode change port in `serial4wire.py` with one your arduino is connected 
```
import code
import serial
from enum import Enum

# Change port here.
PORT = '/dev/ttyACM0'

...
```

### 3 Wire Serial Interface
To use this tool for 3 wire serial interface uncomment the following in sketch `4WireSerial/4WireSerial.ino`
```
// Uncomment the following to use 3 wire serial interface.
//#define THREE_WIRESERIAL

...
```

### Change default pins
Default pins are:
+ strobe 7
+ clock 8
+ data_in 9 (Same as data_in/out in 3 wire serial interface.)
+ data_out 10

Change default pins in `4WireSerial/4WireSerial.ino`
```
...

// Change pins here
#define STROBE_PIN 7
#define CLOCK_PIN 8
#define DATA_IN_PIN 9
#define DATA_OUT_PIN 10 // Ignore if using 3 wire serial interface.

...
```

## Preparation

1) Compile and upload sketch present in `4WireSerial` to your arduino using Arduino IDE or Arduino CLI.
2) Connect your 3/4-wire serially interfaced device to arduino at default pins or at your custom pins to Arduino.
3) Connect your Arduino to PC. 

    
## Usage
### API
Import serial4wire in your project.
### `class serial4wire.SerialDevice`
> \_\_init__(port)

`Parameters`:

port - Port name. eg.
+ Windows: COM1, COM2, COM3 etc...
+ Linux: /dev/ttyXXXX
+ macOS: /dev/tty.XXXX

Will wait untill the port is opened at given port name.
Make sure you provide correct port name or it will stall your code.

> send(*data:int)

`Parameters`:  

*data - Data in ints to send. (Note: All ints must be 8bit integer.)

`Returns`: Number of bytes sent.  
`Return type`: int

Sends given integers byte by byte serially to your 3/4-wire serially interfaced device.  
Note: Strobe value is not changed in process.

> recv(count:int=1)

`Parameters`:

count - Number of bytes to receive.

`Returns`: Tuple of received bytes.  
`Return type`: tuple

Receives bytes from device serially and returns received bytes in tuple.  
Note: Strobe value is not changed in process.

> stb(val:bool)

`Parameters`:

val - value to set at strobe pin.

`Returns`: Nothing  

Sets strobe pin value. True=HIGH, False=LOW.  

> send_str(string:str)

`Parameters`:

string -  String to send.

`Returns`: Number of bytes sent.  
`Return type`: int

Sends string in ascii encoded format.
Note: Strobe value is not changed in process.

> send_cmd(cmd:int, *data:int)

`Parameters`:

cmd - Command to send.  
data - Data to send following the command.

`Returns`: Number of bytes sent.  
`Return type`: int

Sets strobe LOW then sends data following the command then sets strobe HIGH.
If data = (), only command is sent.

> recv_data(cmd:int, count:int)

`Parameters`: 

cmd - Command to send before receiving data from device.
count - Number of bytes to receive.

`Returns`: Tuple of received bytes.  
`Return type`: tuple

Sets strobe LOW then sends command before receiving data then sets strobe HIGH.
### Interactive Mode
Executing `serial4wire.py` by itself will start an interactive console after connecting to device
at port configured above. You can then use wrapper functions provided by same name as above API 
to communicate with your serial device. These wrapper function don't return anything but are more verbose. For eg.  
```
[4WireSerial] Waiting for device at port: /dev/ttyACM0
[4WireSerial] Port opened at: /dev/ttyACM0
[4WireSerial] Starting interactive console:

>>> send_cmd(0x42, *(0xFF,)*4)

      HEX  BIN        DEC
[CMD] 42 : 01000010 : 066
[001] FF : 11111111 : 255
[002] FF : 11111111 : 255
[003] FF : 11111111 : 255
[004] FF : 11111111 : 255

5 Byte(s) sent.
```






