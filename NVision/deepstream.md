samples path: /opt/nvidia/deepstream/deepstream-6.0

Installing triton directly onto the machine  
ReadMe in directory : /opt/nvidia/deepstream/deepstream-6.0/samples/configs


Deepstream Triton container image has Triton Inference Server and supported
backend libraries pre-installed. But in case of Jetson to run the Triton
Inference Server direclty on device, Triton Server setup will be required.
1. Go to samples directory and run the following command to set up the Triton
   Server and backends.
   $ sudo ./triton_backend_setup.sh

Notes:
   By default script will download the Triton Server version 2.13. For setting
   up any other version change the package path accordingly.

   Triton release version: 21.07

   https://github.com/triton-inference-server/server/releases?page=4
   