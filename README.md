# Project Overview

This repository contains the content for a proof of concept implementation of computer vision systems in the industry. The project explores scalability and performance using the NVIDIA ecosystem, aiming to create an example scaffold for implementing a system accessible to non-technical users.

---

## Hardware Used

### Host Machine
- Machine: Personal Computer
- CPU: Ryzen 5600X
- GPU: EVGA RTX 2070 Super 8GB
- RAM: 16 GB DDR4
- OS: Ubuntu 22.04

#### Drivers
- CUDA Version: **12.3**
- CuDNN: **8**
- Driver Version: **545.23.08**

### Client Machine
- Machine: CONNECTTECH Rudi AGX Xavier
- CPU: ARMv8
- GPU: iGPU 
- RAM: 32 GB
- OS: Jetpack **4.6.2** (L4T **32.7.2**)

#### Drivers
- CUDA Version: **10.2**
- CuDNN: **8**
- TensorRT: **8.2.1.8**

---

## Software Implementations

### Host Machine

#### <span style="color:#005F99">NVision</span>
- **Function:** Automation Of Model Creation
- **Supported Frameworks:** 
  - **<span style="color:#008000">Tensorflow2</span>**
  - **<span style="color:#FF0000">Tensorflow1</span>**
  - **<span style="color:#FF0000">PyTorch</span>**
  - **<span style="color:#FF0000">TensorRT</span>**
  - **<span style="color:#FF0000">ONNX</span>**
- **Language:** Python, Docker

#### <span style="color:#005F99">OVision</span>
- **Function:** Host Frontend CV Management System
- **Framework:** Angular **16**
- **Language:** HTML, SASS, TypeScript, Docker

#### <span style="color:#005F99">Postgres</span>
- **Function:** Host Database Implementation
- **Framework:** PostgreSQL **16.2**
- **Language:** PSQL, bash, Docker

#### <span style="color:#005F99">VisionLinkAPI</span>
- **Function:** Host API For Communication Between Instances
- **Framework:** NodeJS **16**
- **Language:** TS (written), JS (compiled)

### Client Machine

#### <span style="color:#008000">Triton</span>
- **Function:** Host Triton Inference Server For Model Serving
- **Language:** Docker


