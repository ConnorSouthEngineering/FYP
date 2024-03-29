import os
import getpass
import requests
import docker
from time import sleep
import shutil

async def get_task_data(task_id):
    task_result = requests.get(f"http://localhost:3000/tasks/{task_id}")
    task = task_result.json()[0]['get_task'][0]
    return task

def check_for_image(image_tag,client):
    images = client.images.list()
    for image in images:
        try:
            if(f'{image_tag}:latest' == str(image.attrs['RepoTags'][0])):
                return True
        except:
            pass
        return False

def build_cudatf_image(client, image_tag):
    response = client.images.build(path=".", tag=image_tag, rm=True)
    return response
    
async def launch_container(image_tag, task_id, folder_name):
    client = docker.from_env()
    task = await get_task_data(task_id)
    abs_path = f'/home/{getpass.getuser()}/Desktop/FYP/master/NVision'
    key_path = f'/home/{getpass.getuser()}/api.key'
    model_name = f"{task['model_name']}_{task_id}"
    entry_cmd = ["python3", "train_model.py",
             "--model_name", model_name,
             "--epochs", str(task['epochs']),
             "--num_frames", str(task['num_frames']),
             "--shuffle_size", str(task['shuffle_size']),
             "--batch_size", str(task['batch_size'])]
    volume_mapping = {
                  f"{abs_path}/model_tasks/{folder_name}": {'bind': '/mnt', 'mode': 'rw'},  
                  f"{abs_path}/model_repo": {'bind': '/model_repo', 'mode': 'rw'},
    }
    debug_mode = True

    try:
        response = client.login(registry="https://nvcr.io", username="$oauthtoken", password=(open(key_path, "r").read()))

        
        if debug_mode or not check_for_image(image_tag,client):
            print("Building cudatf image...")
            build_result = build_cudatf_image(client, image_tag)
        
        container = client.containers.run(f"{image_tag}:latest", 
                            name=model_name, 
                            detach=True,
                            device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])],
                            tty=True, 
                            stdin_open=True, 
                            entrypoint=entry_cmd,
                            volumes=volume_mapping)
        file = f'{model_name}_training_confusion.png'
        file_status = False
        while not file_status:
            present_files = []
            path = f'../model_repo/{model_name}/1/model.savedmodel/assets/{file}'
            if os.path.exists(path):
                if os.path.isfile(path):
                    file_status = True
                else:
                    sleep(5)
                    print("files missing")
            else:
                sleep(5)
                print("files missing")
        container.stop()
        container.remove()
        return [True,model_name]
    except docker.errors.ContainerError as e:
        print(f"Container run error: {e}")
        return [False,model_name]
    except docker.errors.ImageNotFound as e:
        print(f"Image not found error: {e}")
        return [False,model_name]
    except docker.errors.APIError as e:
        print(f"Docker API error: {e}")
        return [False,model_name]
