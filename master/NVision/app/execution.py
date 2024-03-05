from aiohttp import web
import asyncio

from modules.pull_files import pull_files
from modules.dockerise_model import launch_container
from modules.task_orders import update_task_status, create_model_entry

async def create_model(request):
    body = await request.json()
    print(body)
    task_id = body[0]['insert_model_task']
    print(task_id)
    update_task_status(task_id,"gathering")
    image_tag = "cudatf"  
    files_task = asyncio.create_task(pull_files(task_id))
    await files_task
    folder_name = files_task.result()
    update_task_status(task_id,"training")
    container_task = asyncio.create_task(launch_container(image_tag, task_id, folder_name))
    await container_task
    if(container_task.result()):
        update_task_status(task_id,"trained")
        print("Success")
    else:
        update_task_status(task_id,"failed")
        return web.Response(text=f"Task {task_id} has failed")
    creation_task = asyncio.create_task(create_model_entry(task_id, folder_name))
    await creation_task
    if(creation_task.result()):
        update_task_status(task_id,"trained")
        print("Success")
    else:
        update_task_status(task_id,"failed")
        return web.Response(text=f"Task {task_id} has failed")
    return web.Response(text=f"Task {task_id} has succeeded")
    
    

async def request_model(request):
    body = await request.json()
    model_id = body['model_id']

async def server_up():
    server = '0.0.0.0'
    port = 8080
    app = web.Application()
    app.add_routes([web.post('/model/create', create_model)])
    app.add_routes([web.post('/model/request', request_model)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, server, port)
    await site.start()
    print(f"Server ready to recieve model requests http://{server}:{port}")

async def main():
    await server_up()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
