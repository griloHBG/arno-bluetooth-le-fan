#!/usr/bin/python3
"""
Arno Ventilador Bluetooth

Tentando né...
"""

import sys
import asyncio

from bleak import BleakClient
from pathlib import Path

ADDRESS = "A4:C1:38:03:0C:4C"
fan_memory_file = Path('/tmp/arno-bluetooth-fan-last-speed')

"""
[NEW] Primary Service (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service0008
        00001801-0000-1000-8000-00805f9b34fb
        Generic Attribute Profile
[NEW] Characteristic (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service0008/char0009
        00002a05-0000-1000-8000-00805f9b34fb
        Service Changed
[NEW] Descriptor (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service0008/char0009/desc000b
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Primary Service (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service000c
        0000180a-0000-1000-8000-00805f9b34fb
        Device Information
[NEW] Characteristic (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service000c/char000d
        00002a50-0000-1000-8000-00805f9b34fb
        PnP ID
[NEW] Primary Service (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service000f
        01000000-8000-1000-8000-111111111111
        Vendor specific
[NEW] Characteristic (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service000f/char0010
        02000000-8000-1000-8000-111111111111
        Vendor specific
[NEW] Descriptor (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service000f/char0010/desc0012
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Descriptor (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service000f/char0010/desc0013
        00002901-0000-1000-8000-00805f9b34fb
        Characteristic User Description
[NEW] Characteristic (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service000f/char0014
        03000000-8000-1000-8000-111111111111
        Vendor specific
[NEW] Descriptor (Handle 0x0000)
        /org/bluez/hci0/dev_A4_C1_38_03_0C_4C/service000f/char0014/desc0016
        00002901-0000-1000-8000-00805f9b34fb
        Characteristic User Description
"""

"""
 $ python3 bleak_service_explorer.py --address a4:c1:38:03:0c:4c
2023-10-30 00:52:51,770 __main__ INFO: starting scan...
2023-10-30 00:52:52,541 __main__ INFO: connecting to device...
2023-10-30 00:52:53,030 __main__ INFO: connected
2023-10-30 00:52:53,031 __main__ INFO: [Service] 0000180a-0000-1000-8000-00805f9b34fb (Handle: 12): Device Information
2023-10-30 00:52:53,118 __main__ INFO:   [Characteristic] 00002a50-0000-1000-8000-00805f9b34fb (Handle: 13): PnP ID (read), Value: bytearray(b'\x02\x8a$f\x82\x01\x00')
2023-10-30 00:52:53,119 __main__ INFO: [Service] 01000000-8000-1000-8000-111111111111 (Handle: 15): Unknown
2023-10-30 00:52:53,119 __main__ INFO:   [Characteristic] 03000000-8000-1000-8000-111111111111 (Handle: 20): Unknown (write)
2023-10-30 00:52:53,152 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 22): Characteristic User Description, Value: bytearray(b'Fan Control Out\x00')
2023-10-30 00:52:53,180 __main__ INFO:   [Characteristic] 02000000-8000-1000-8000-111111111111 (Handle: 16): Unknown (read,notify), Value: bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
2023-10-30 00:52:53,217 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 19): Characteristic User Description, Value: bytearray(b'Fan Control In\x00')
2023-10-30 00:52:53,236 __main__ INFO:     [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 18): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
2023-10-30 00:52:53,236 __main__ INFO: [Service] 00001801-0000-1000-8000-00805f9b34fb (Handle: 8): Generic Attribute Profile
2023-10-30 00:52:53,237 __main__ INFO:   [Characteristic] 00002a05-0000-1000-8000-00805f9b34fb (Handle: 9): Service Changed (indicate)
2023-10-30 00:52:53,274 __main__ INFO:     [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 11): Client Characteristic Configuration, Value: bytearray(b'\x02\x00')
2023-10-30 00:52:53,274 __main__ INFO: disconnecting...
2023-10-30 00:52:55,937 __main__ INFO: disconnected
"""

GENERIC_ATTRIBUTE_PROFILE               = "00001801-0000-1000-8000-00805f9b34fb" # 00:00:18:01:00:00:10:00:80:00:00:80:5f:9b:34:fb
SERVICE_CHANGED                         = "00002a05-0000-1000-8000-00805f9b34fb" # 00:00:2a:05:00:00:10:00:80:00:00:80:5f:9b:34:fb
CLIENT_CHARACTERISTC_CONFIGURATION_1    = "00002902-0000-1000-8000-00805f9b34fb" # 00:00:29:02:00:00:10:00:80:00:00:80:5f:9b:34:fb
DEVICE_INFORMATION                      = "0000180a-0000-1000-8000-00805f9b34fb" # 00:00:18:0a:00:00:10:00:80:00:00:80:5f:9b:34:fb
PNP_ID                                  = "00002a50-0000-1000-8000-00805f9b34fb" # 00:00:2a:50:00:00:10:00:80:00:00:80:5f:9b:34:fb
VENDOR_SPECIFIC_1                       = "01000000-8000-1000-8000-111111111111" # 01:00:00:00:80:00:10:00:80:00:11:11:11:11:11:11
VENDOR_SPECIFIC_2                       = "02000000-8000-1000-8000-111111111111" # 02:00:00:00:80:00:10:00:80:00:11:11:11:11:11:11 # this one is present on bt log from Android to arno ventilador
CLIENT_CHARACTERISTC_CONFIGURATION_2    = "00002902-0000-1000-8000-00805f9b34fb" # 00:00:29:02:00:00:10:00:80:00:00:80:5f:9b:34:fb
CHARACTERISTIC_USER_DESCRIPTION         = "00002901-0000-1000-8000-00805f9b34fb" # 00:00:29:01:00:00:10:00:80:00:00:80:5f:9b:34:fb
VENDOR_SPECIFIC_3                       = "03000000-8000-1000-8000-111111111111" # 03:00:00:00:80:00:10:00:80:00:11:11:11:11:11:11 # this one is present on bt log from Android to arno ventilador
CHARACTERISTC_USER_DESCRIPTION          = "00002901-0000-1000-8000-00805f9b34fb" # 00:00:29:01:00:00:10:00:80:00:00:80:5f:9b:34:fb

async def main(address):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")
        
        ##this is failing!
        #paired = await client.pair(protection_level=2)
        #print(f"Paired: {paired}")

        #print(f"is connected: {client.is_connected}")
        #print(f"2 - Turning it on...  {VENDOR_SPECIFIC_2}")
        #await client.write_gatt_char(VENDOR_SPECIFIC_2, bytearray([0x00,0x03]), response=True)
        #print(f"is connected: {client.is_connected}")
        #await asyncio.sleep(3.0)

        #print(f"is connected: {client.is_connected}")
        #print(f"2 - Turning it off... {VENDOR_SPECIFIC_2}")
        #await client.write_gatt_char(VENDOR_SPECIFIC_2, bytearray([0x00,0x00]), response=True)
        #print(f"is connected: {client.is_connected}")
        #await asyncio.sleep(3.0)
        
        ## this is too slow...
        #current_speed = await client.read_gatt_char(VENDOR_SPECIFIC_2)
        #current_speed = current_speed[2]
        #print(current_speed)

        if not fan_memory_file.exists():
            fan_memory_file.write_text("0")
        
        current_speed = int(fan_memory_file.read_text())
        
        current_speed -= 1
        print(current_speed)

        current_speed = 3 if current_speed < 0 else current_speed
        print(current_speed)

        print(f"is connected: {client.is_connected}")
        print(f"3 - Setting speed {current_speed}... {VENDOR_SPECIFIC_3}")
        await client.write_gatt_char(VENDOR_SPECIFIC_3, bytearray([0, current_speed]), response=True)
        print(f"is connected: {client.is_connected}")

        fan_memory_file.write_text(f"{current_speed}")

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
