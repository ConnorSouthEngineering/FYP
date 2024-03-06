import os
import docker
import getpass

# Define the path to the Dockerfile and build context
build_context_path = os.path.join(os.getenv("HOME"), "Desktop/FYP/node/XInference")

# Initialize the Docker client
client = docker.from_env()

# Path to the API key
key_path = os.path.join('/home', getpass.getuser(), 'api.key')

# Login to the Docker registry
with open(key_path, "r") as key_file:
    api_key = key_file.read().strip()  # Remove any newline characters
response = client.login(registry="nvcr.io", username="$oauthtoken", password=api_key)
print(f"Login response: {response}")

# Build the Docker image
try:
    # Start the build process
    image, build_logs = client.images.build(path=build_context_path, tag="test_python", rm=True)
    print(f"Build succeeded: {image.tags}")

    # Print build logs
    for log in build_logs:
        if 'stream' in log:
            print(log['stream'].strip())

except docker.errors.BuildError as build_err:
    print("Build failed:")
    for log in build_err.build_log:
        if 'stream' in log:
            print(log['stream'].strip())
except Exception as ex:
    print(f"Unexpected error during build: {ex}")
