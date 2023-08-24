
// Uncomment the following to use 3 wire serial interface.
//#define THREE_WIRESERIAL

// Change pins here
#define STROBE_PIN 7
#define CLOCK_PIN 8
#define DATA_IN_PIN 9
#define DATA_OUT_PIN 10 // Ignore if using 3 wire serial interface.


const byte stb = STROBE_PIN;
const byte clk = CLOCK_PIN;
const byte dataIn = DATA_IN_PIN;

#ifndef THREE_WIRESERIAL
const byte dataOut = DATA_OUT_PIN;

#else
const byte dataOut = DATA_IN_PIN;

#endif

enum CMD {
    SEND = 'S',
    READ = 'R',
    STB_HIGH = 'H',
    STB_LOW = 'L'
};

void sendBytes(byte* buf, byte count);
void recvBytes(byte* buf, byte count);

void setup() {

    Serial.begin(9600);
    
    pinMode(stb, OUTPUT);
    pinMode(clk, OUTPUT);

    digitalWrite(stb, HIGH);
}

void loop() {

    if(Serial.available()) {

        byte cmd = Serial.read();
                
        if(cmd == CMD::SEND) {
            
            while(!Serial.available()) {}
            byte count = Serial.read();

            byte* buffer = new byte[count];

            byte received = Serial.readBytes(buffer, count);
            sendBytes(buffer, count);
            Serial.write(received);

            delete [] buffer;
        }

        else if(cmd == CMD::READ) {
           
            while(!Serial.available()) {}
            byte count = Serial.read();

            byte* buffer = new byte[count];

            recvBytes(buffer, count);
            Serial.write(buffer, count);

            delete [] buffer;
        }

        else if(cmd == CMD::STB_HIGH) {
            
            digitalWrite(stb, HIGH);
            Serial.write(0x00); //ACK
        }

        else if(cmd == CMD::STB_LOW) {

            digitalWrite(stb, LOW);
            Serial.write(0x00); //ACK
        }
    }
}

void sendBytes(byte* buf, byte count) {

    delayMicroseconds(10);
    pinMode(dataIn, OUTPUT);
    digitalWrite(clk, LOW); // Writing data on rising edges.

    for(int i = 0; i < count; i++)
        shiftOut(dataIn, clk, LSBFIRST, buf[i]);

    delayMicroseconds(10);
}

void recvBytes(byte* buf, byte count) {
    
    delayMicroseconds(10);
    pinMode(dataOut, INPUT_PULLUP);
    digitalWrite(clk, HIGH); // Reading data on falling edges.

    for(int i = 0; i < count; i++)
        buf[i] = shiftIn(dataOut, clk, LSBFIRST);

    delayMicroseconds(10);
}
