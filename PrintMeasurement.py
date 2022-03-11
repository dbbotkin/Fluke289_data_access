# ******************************************************************************
# Fluke 287 data logger
# 2020 Grease monkey - No rights reserved {++THANK YOU FROM DBBOTKIN}
# ******************************************************************************
import serial
import time

ser = serial.Serial()

# Setup logging
ser.port = '/dev/cu.usbserial-AC00FZQJ'    # MY Serial port; find your . . .
logging_period = 1 # seconds
no_of_records = 5 # how many records to record


# Serial port setup and open
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.timeout = 0.1  # seconds
try:
    ser.open()
except:
    print("Cannot open serial port...")
    exit()

dmm_response_ok = 1
measurements = list()
measurement = 0.0


# This starts a thread every N seconds
def logger():
    global no_of_records
    global dmm_response_ok
    global measurements


    # Check if the last response was valid
    if dmm_response_ok == 0:
        print("DMM not responding. Check connections and make sure that the dmm is turned on")
    if no_of_records >= 0 and dmm_response_ok:
        for i in range (0, no_of_records):
        #Make a measurement, decode it and print        
            measurement = decode_response(read_with_qm())
            print (str(measurement)[1:6])
            time.sleep(logging_period)


# Send 'QM' command and read the response
def read_with_qm():
    # Flush buffers and send command in ASCII
    ser.flushInput()
    ser.flushOutput()
    ser.write(('QM' + '\r').encode('utf-8'))
    # Define End Of Line character
    response = b''
    second_eol = False
    # Read the response
    while True:
        # Fetch a character from the receive buffer
        c = ser.read(1)
        if c:
            # Append characters to response
            response += c
            if c == b'\r':
                # Break when the second EOL comes
                if second_eol:
                    break
                else:
                    # When the first EOL comes set the second_eol flag True
                    second_eol = True
        else:
            break
    return response


# Decode the dmm's response and return a list
def decode_response(response):
    global dmm_response_ok
    measurement_list = list()

    if len(response) > 0:
        response_string = response.decode("utf-8")        
        response_split = response_string.split('\r')
        # Check if there are two '/r'
        if len(response_split) == 3:
            # CMD_ACK

            measurement_split = response_split[1].split(',')
            if len(measurement_split) == 4:
                # Value
                measurement_list.append(float(measurement_split[0]))
                # Unit
#                measurement_list.append(measurement_split[1])
                # State
#                measurement_list.append(measurement_split[2])
                # Attribute
 #               measurement_list.append(measurement_split[3])
                return measurement_list
            else:
                print("Exiting. Incorrect no of items...")
                dmm_response_ok = 0
        else:
            print("Exiting. Incorrect no of '\\r's...")
            dmm_response_ok = 0
    else:
        print("Exiting. No response from dmm...")
        dmm_response_ok = 0




# Start logging
logger()

