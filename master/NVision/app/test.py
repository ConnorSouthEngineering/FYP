import docker
client = docker.from_env()
images = client.images.list()
for image in images:
    try:
        print(image.attrs['RepoTags'][0])
    except:
        pass
