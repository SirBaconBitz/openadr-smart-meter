# Quick code to test smart meter connectivity
# Imports required for physical meter usage
import minimalmodbus
import serial
from time import time

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

ElecCurrent = instrument.read_register(4000,2)
print(ElecCurrent)