from jtop import jtop
import aiofiles
import datetime
import asyncio
from aiocsv import AsyncDictWriter
import os

async def compile_performance_entry(jetson, csv_log, description):
    log_dict = {"Timestmp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),"Event":description,"Total CPU utilisation %":jetson.cpu['total']['user']+jetson.cpu['total']['nice']+jetson.cpu['total']['system'],"Total CPU RAM utilisation %":(jetson.memory['RAM']['used']/jetson.memory['RAM']['tot'])*100,"Total GPU utilisation %":jetson.gpu['gv11b']['status']['load'],"Total GPU RAM utilisation %":(jetson.memory['RAM']['shared']/jetson.memory['RAM']['tot'])*100,"Total Swap Utilisation %":(jetson.memory['SWAP']['used']/jetson.memory['SWAP']['tot'])*100}
    csv_log.append(log_dict)

async def dump_logs(csv_log, file_name):
    print(f"Dumping logs {file_name}")
    while True:
        file_exists = os.path.isfile(file_name)
        fields = ["Timestmp","Event","Total CPU utilisation %","Total CPU RAM utilisation %","Total GPU utilisation %","Total GPU RAM utilisation %","Total Swap Utilisation %"]
        async with aiofiles.open(file_name, mode='a') as log:
            writer = AsyncDictWriter(log, fieldnames=fields)
            if not file_exists:
                await writer.writeheader()
            for row in csv_log:
                await writer.writerow(row)
            csv_log.clear()
        await asyncio.sleep(3)
    