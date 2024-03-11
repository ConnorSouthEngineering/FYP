from aiohttp import web
import asyncio

from modules.gstreamer import update_system_cameras, get_cameras

camera_task = None

async def launch_inference():
    print("Launch inference")

async def server_up():
    server = '0.0.0.0'
    port = 2500
    app = web.Application()
    app.add_routes([web.post('/triton/initialise_deployment', launch_inference)])
    app.add_routes([web.get('/node/cameras', get_cameras)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, server, port)
    await site.start()
    global camera_task
    camera_task = loop.create_task(update_system_cameras())
    print(f"Server ready to recieve model requests http://{server}:{port}")

async def main():
    await server_up()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
