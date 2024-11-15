from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# Create a Modbus datastore
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17] * 100),
    co=ModbusSequentialDataBlock(0, [17] * 100),
    hr=ModbusSequentialDataBlock(0, [17] * 100),
    ir=ModbusSequentialDataBlock(0, [17] * 100),
)
context = ModbusServerContext(slaves=store, single=True)

# Set device identification (optional)
identity = ModbusDeviceIdentification()
identity.VendorName = "pymodbus"
identity.ProductCode = "PM"
identity.VendorUrl = "http://github.com/riptideio/pymodbus/"
identity.ProductName = "pymodbus Server"
identity.ModelName = "pymodbus Server"
identity.MajorMinorRevision = "1.0"

# Start Modbus server on port 5000
print("Starting Modbus server on port 5000...")
StartTcpServer(context, identity=identity, address=("0.0.0.0", 5000))

