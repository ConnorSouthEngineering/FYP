from aiohttp import web
import asyncio
import docker
from docker.errors import ImageNotFound, BuildError, APIError
from time import sleep
import tarfile
import io
import subprocess

from data_set_creation.pull_files import pull_files

async def build_image(image_tag, dockerfile_path="."):
    client = docker.from_env()
    try:
        client.images.build(path=dockerfile_path, tag=image_tag, rm=True)
        print(f"Image {image_tag} built successfully.")
    except BuildError as e:
        print(f"Error building image: {e}")
    except APIError as e:
        print(f"Docker API error: {e}")

async def launch_container(image_tag, container_name):
    client = docker.from_env()
    try:
        client.containers.run(image_tag, name=container_name, detach=True,
                              device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])],
                              tty=True, stdin_open=True)
        print(f"Container {container_name} started.")
        file_status = False
        while not file_status:
            container = client.containers.get(container_name)
            command = "/bin/sh -c 'test -f test.h5 && echo exists || echo not exists'"
            exit_code, output = container.exec_run(command)
            print(f"Exit code: {exit_code}, Output: {output.decode()}")
            output = output.decode().strip()
            
            if output == "exists":
                print("File test.h5 exists.")
                file_status = True
                stream, _ = container.get_archive("home/test.h5")
                file_like_object = io.BytesIO()
                
                for chunk in stream:
                    file_like_object.write(chunk)
                
                file_like_object.seek(0)

                with tarfile.open(fileobj=file_like_object, mode='r') as tar:
                    member = tar.next()
                    if member is not None and member.name.endswith("test.h5"):
                        with tar.extractfile(member) as extracted_file:
                            with open("./extract_model.h5",'wb') as outfile:
                                outfile.write(extracted_file.read())
                container.stop()
                container.remove()
                
            else:
                print("File /home/test.h5 does not exist. Checking again in 5 seconds...")
                sleep(5)

    except docker.errors.ContainerError as e:
        print(f"Container run error: {e}")
    except docker.errors.ImageNotFound as e:
        print(f"Image not found error: {e}")
    except docker.errors.APIError as e:
        print(f"Docker API error: {e}")

async def launch_model(request):
    body = await request.json()
    task_id = body['task_id']
    image_tag = "cudatf:Dockerfile"  
    container_name = f'model_container_{task_id}'
    
    folder_name = pull_files(task_id)

    #asyncio.create_task(launch_container(image_tag, container_name))
    return web.Response(text=f"Task {task_id} is being processed in the background!")

async def server_up():
    app = web.Application()
    app.add_routes([web.post('/model', launch_model)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print("Server ready to recieve model requests http://localhost:8080")

async def main():
    await server_up()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
