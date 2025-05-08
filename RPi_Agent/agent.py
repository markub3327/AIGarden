import asyncio
import struct
from bleak import BleakScanner, BleakClient
from influxdb_client_3 import Point, InfluxDBClient3

# Define UUIDs for characteristics
CHARACTERISTICS = {
    "battery_voltage": "19B11A01-F8F2-537E-4F6C-D104768A1215",
    "solar_voltage": "19B11A02-F8F2-537E-4F6C-D104768A1215",
    "soil_kiwi": "19B11B01-F8F2-537E-4F6C-D104768A1215",
    "soil_pelargonium": "19B11B02-F8F2-537E-4F6C-D104768A1215",
    "temperature": "19B11C01-F8F2-537E-4F6C-D104768A1215",
    "humidity": "19B11C02-F8F2-537E-4F6C-D104768A1215",
    "pressure": "19B11C03-F8F2-537E-4F6C-D104768A1215",
    "altitude": "19B11C04-F8F2-537E-4F6C-D104768A1215",
    "water_level": "19B11E01-F8F2-537E-4F6C-D104768A1215",
    "charger_fault": "19B11D02-F8F2-537E-4F6C-D104768A1215",
    "charger_charge": "19B11D01-F8F2-537E-4F6C-D104768A1215",
}

# BLE target
TARGET_NAME = "AIGarden"

# InfluxDB credentials
INFLUXDB_URL = "http://localhost:8181"
INFLUXDB_TOKEN = "apiv3_Xt_e04hbvSMpZYofueUcbM_Z7GnfI4K5E32PtGw9k9gOIuonpOhDMBHHOzi9SrvyH1Kbfp-dAjiUWhoFi2QHow"
INFLUXDB_ORG = "home"
INFLUXDB_DB = "ai_garden"

client = InfluxDBClient3(host=INFLUXDB_URL,
                         database=INFLUXDB_DB,
                         token=INFLUXDB_TOKEN,)

async def find_device(name=TARGET_NAME, timeout=30):
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=timeout)
    for device in devices:
        if name in device.name:
            print(f"Found {name} at address {device.address}")
            return device.address
    print("Device not found.")
    return None

def parse_float(data: bytearray) -> float:
    return round(struct.unpack('<f', data)[0], 2)

def handle_notification(key, is_float=False):
    def handler(sender, data):
        value = parse_float(data) if is_float else data[0]
        # Store in InfluxDB
        point = (
            Point("home")
            .tag("room", "Balcony")
            .field(key, value)
        )
        client.write(point)
#        print(f"✅ Data written to InfluxDB. {key}")
    return handler

async def subscribe_to_notifications(address):
    try:
        async with BleakClient(address) as client:
            if not client.is_connected:
                 print("❌ Failed to connect.")
                 return

            print("✅ Connected to BLE device. Listening for updates...")

            # Subscribe to characteristics
            await client.start_notify(CHARACTERISTICS["battery_voltage"], handle_notification("battery_voltage", True))
            await client.start_notify(CHARACTERISTICS["solar_voltage"], handle_notification("solar_voltage", True))
            await client.start_notify(CHARACTERISTICS["soil_kiwi"], handle_notification("soil_kiwi"))
            await client.start_notify(CHARACTERISTICS["soil_pelargonium"], handle_notification("soil_pelargonium"))
            await client.start_notify(CHARACTERISTICS["temperature"], handle_notification("temperature", True))
            await client.start_notify(CHARACTERISTICS["humidity"], handle_notification("humidity", True))
            await client.start_notify(CHARACTERISTICS["pressure"], handle_notification("pressure", True))
            await client.start_notify(CHARACTERISTICS["altitude"], handle_notification("altitude", True))
            await client.start_notify(CHARACTERISTICS["water_level"], handle_notification("water_level"))
            await client.start_notify(CHARACTERISTICS["charger_fault"], handle_notification("charger_fault"))
            await client.start_notify(CHARACTERISTICS["charger_charge"], handle_notification("charger_charge"))

            while client.is_connected:
                await asyncio.sleep(60)  # keep running and receiving notifications until connection ends

    # except BleakError as e:
    #     print(f"❌ BLE Error: {e}")
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")

async def main():
    address = await find_device()
    if not address:
        return

    while True:
        await subscribe_to_notifications(address) 
        print("🔁 Attempting reconnection in 5 seconds...")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

