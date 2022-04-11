# This version of the client pulls data from a physical smart meter rather than a file
import asyncio
from datetime import timedelta
from openleadr import OpenADRClient, enable_default_logging
import random
import sys
from meters.meter import meterclass as m
from vectn.vecgen import vecgenclass as vgen
enable_default_logging()

# Imports required for physical meter usage
import minimalmodbus
import serial
from time import time

# Credit to Trey Burks, Bradley Northern, and Dr. Denis Ulybyshev for their contributions
# to the MinimalModbus portion of the code
# Definition of Modbus instrument to pull data from
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)

# Serial setting of Modbus instrument
instrument.serial.port = '/dev/ttyUSB0'     # Serial port name
instrument.serial.baudrate = 9600           # Baudrate of device
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE   # Parity of device (EVEN, ODD, NONE, etc.)
instrument.serial.stopbits = 1
instrument.serial.timeout = 1               # Timeout defined in seconds

# Other instrument settings
instrument.debug = True                     # Enable debug in console
instrument.address = 1                      # Slave address of device
instrument.mode = minimalmodbus.MODE_RTU    # Set transmission mode to Modbus RTU (ASCII also offered)
instrument.clear_buffers_before_each_transaction = True
instrument.serial.setRTS(1)
instrument.serial.setDTR(1)

async def collect_report_value():
    # This callback is called when you need to collect a value for your Report
    # Uses previously defined Modbus instrument to pull and send values
    # Modify according to your needs
    
    # Read up to two decimal places from register 4000 of instrument
    ElecCurrent = instrument.read_register(4000,2)
    
    # Print for confirmation of value
    print("*****************************************************************")
    print(ElecCurrent)
    print("*****************************************************************")
    
    # Return value to send to VTN
    return ElecCurrent

async def read_tcp_pkt():
    msr = random.uniform(1.0, 10.5)
    return msr

async def read_modbus_pkt():
    msr = random.uniform(1.0, 10.5)
    return msr

async def handle_event(event):
    # This callback receives an Event dict.
    # You should include code here that sends control signals to your resources.
    # Check if we can opt in to this event
    first_signal = event['event_signals'][0]
    intervals = first_signal['intervals']
    target = event['target']
    print("Event is: ", event)
    print("\n Signal name is : ", first_signal)
    return 'optIn'


# Create the client object
# Adjust the vtn_url parameter to whatever the IP address and port of the VTN are
# Ex. 'http://192.168.10.15:8080/OpenADR2/Simple/2.0b'
client = OpenADRClient(ven_name='ven123',
                       vtn_url='http://localhost:8080/OpenADR2/Simple/2.0b')

# Add the report capability to the client
client.add_report(callback=collect_report_value,
                  resource_id='device001',
                  measurement='voltage',
                  sampling_rate=timedelta(seconds=5))


# Add event handling capability to the client
client.add_handler('on_event', handle_event)

# Run the client in the Python AsyncIO Event Loop
loop = asyncio.get_event_loop()
loop.create_task(client.run())
loop.run_forever()


