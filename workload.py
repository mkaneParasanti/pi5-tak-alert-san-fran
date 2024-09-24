#!/bin/bash

import asyncio
import xml.etree.ElementTree as ET
from configparser import ConfigParser
import pytak
import gpiod
from gpiod.line import Direction, Value

LED_PIN = 14
PIR_PIN = 4
CHIP_PATH = '/dev/gpiochip4'


class MySerializer(pytak.QueueWorker):
    """
    Defines how you process or generate your Cursor on Target Events.
    From there it adds the CoT Events to a queue for TX to a COT_URL.
    """

    async def handle_data(self, data):
        """Handle pre-CoT data, serialize to CoT Event, then puts on queue."""
        event = data
        await self.put_queue(event)

    async def run(self, number_of_iterations=-1):
        """Run the loop for processing or generating pre-CoT data."""
        while True:
            pir_state = get_line_value(CHIP_PATH,PIR_PIN)
            if pir_state == Value.ACTIVE: 
                data = tak_pong()
                self._logger.info("Sending:\n%s\n", data.decode())
                await self.handle_data(data)
                await asyncio.sleep(2)
                toggle_line_value(CHIP_PATH,LED_PIN,Value.ACTIVE)
                while get_line_value(CHIP_PATH,PIR_PIN) == 1:
                    await asyncio.sleep(0.1)  # Check every 0.1 seconds
                toggle_line_value(CHIP_PATH,LED_PIN,Value.INACTIVE)

def get_line_value(chip_path, line_offset):
    with gpiod.request_lines(
        chip_path,
        consumer="get-line-value",
        config={line_offset: gpiod.LineSettings(direction=Direction.INPUT)},
    ) as request:
        value = request.get_value(line_offset)
        return value

def toggle_line_value(chip_path, line_offset, value):
    value_str = {Value.ACTIVE: "Active", Value.INACTIVE: "Inactive"}

    with gpiod.request_lines(
        chip_path,
        consumer="toggle-line-value",
        config={
            line_offset: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=value
            )
        },
    ) as request:
        request.set_value(line_offset, value)

def tak_pong():
    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", "b-m-p-s-m")
    root.set("uid", "11111111-9356-41c4-8550-f46990aa19f8")
    root.set("how", "h-g-i-g-o")
    root.set("time", pytak.cot_time())
    root.set("start", pytak.cot_time())
    root.set("stale", pytak.cot_time(3600))
    point = ET.SubElement(root, 'point')
    point.set("lat", "37.755729")
    point.set("lon", "-122.447214")
    point.set("hae", "9999999.0")
    point.set("ce", "9999999.0")
    point.set("le", "9999999.0")
    detail = ET.SubElement(root, 'detail')
    status = ET.SubElement(detail, 'status')
    status.set("readiness", "true")
    link = ET.SubElement(detail, 'link')
    link.set("uid", "ANDROID-Parasanti-1")
    link.set("production_time", pytak.cot_time())
    link.set("type", "a-f-G-U-C")
    link.set("parent_callsign", "HOPE")
    link.set("relation", "p-p")
    contact = ET.SubElement(detail, "contact")
    contact.set("callsign", "Parasanti-pi5-san-fran")
    color = ET.SubElement(detail, "color")
    color.set("argb", "-65536")
    precisionlocation = ET.SubElement(detail, "precisionlocation")
    precisionlocation.set("altsrc", "???")
    usericon = ET.SubElement(detail, "usericon")
    usericon.set("iconsetpath", "COT_MAPPING_SPOTMAP/b-m-p-s-m/-65536")
    return ET.tostring(root, encoding="utf-8")


async def main():
    """Main definition of your program, sets config params and
    adds your serializer to the asyncio task list.
    """
    config = ConfigParser()
    config["mycottool"] = {"COT_URL": "tcp://192.168.8.170:8087"}
    config = config["mycottool"]

    # Initializes worker queues and tasks.
    clitool = pytak.CLITool(config)
    await clitool.setup()

    # Add your serializer to the asyncio task list.
    clitool.add_tasks(set([MySerializer(clitool.tx_queue, config)]))

    # Start all tasks.
    await clitool.run()


if __name__ == "__main__":
    asyncio.run(main())
