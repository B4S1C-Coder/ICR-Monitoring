from pyModbusTCP.server import ModbusServer, DataBank
import logging

# Configure logging
logging.basicConfig(filename='modbus_honeypot.log', level=logging.INFO)

# Initialize Modbus server
server = ModbusServer(host="0.0.0.0", port=5000, no_block=True)

# Callback to log read/write access
def log_modbus_action(addr, value, action):
    logging.info(f"Modbus {action} - Address: {addr}, Value: {value}")

# Example: Populate registers with dummy data
DataBank.set_words(0, [100, 200, 300])  # Registers starting at address 0

# Start the server
try:
    print("Modbus honeypot running...")
    server.start()
except Exception as e:
    print(f"Error: {e}")
    server.stop()

