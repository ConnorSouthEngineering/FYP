import getpass
import docker
import os

def check_for_image(image_tag,client):
    images = client.images.list()
    for image in images:
        try:
            if(f'{image_tag}:latest' == str(image.attrs['RepoTags'][0])):
                return True
        except:
            pass
        return False

def build_cudatf_image(client, image_tag,build_context_path):
    response = client.images.build(path=build_context_path, tag=image_tag, rm=True)
    return response
    
def launch_container(image_tag, folder_name):
    client = docker.from_env()
    abs_path = f'/home/{getpass.getuser()}/Desktop/FYP/node/XInference'
    key_path = os.path.join('/home', getpass.getuser(), 'api.key')
    build_context_path = os.path.join(os.getenv("HOME"), "Desktop/FYP/node/XInference") 
    print(key_path)
    volume_mapping = {
                  f"{abs_path}/{folder_name}": {'bind': '/models', 'mode': 'rw'},  
    }
    port_mapping = {8000: 8000, 8001: 8001, 8002: 8002}
    debug_mode = True
    model_name = "triton_test"
    response = client.login(registry="nvcr.io", username="$oauthtoken", password=(open(key_path, "r").read().strip()))
    image = None
    build_result = None
    if debug_mode or not check_for_image(image_tag,client):
        print("Building cudatf image...")
        image, build_result = build_cudatf_image(client, image_tag,build_context_path
                                                 )
    print(image)
    print(build_result)
    input()
    #Need to sort out nvidia docker installation next
    container = client.containers.run(f"{image_tag}:latest", 
                            name=model_name, 
                            detach=True,
                            device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])],
                            ports=port_mapping, 
                            tty=True, 
                            stdin_open=True, 
                            command="tritonserver --model-repository=/models",
                            volumes=volume_mapping)
    input()
    container.stop()
    container.remove()

def main():
    launch_container("triton_test", "model-repo")

main()

"""      """
