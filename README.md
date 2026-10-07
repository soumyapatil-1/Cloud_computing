# Cloud Computing Laboratory Repository

![Course](https://img.shields.io/badge/Course-Cloud%20Computing%20%2F%20Computer%20Networks-blue.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)
![Microservices](https://img.shields.io/badge/Architecture-Microservices-orange.svg)

This repository contains the experiments, implementations, performance analysis,
and laboratory work completed for the **Cloud Computing / Computer Networks Course**.

---

# Table of Contents

1. [Repository Overview](#1-repository-overview)
2. [Experiment 1 - Hypervisor Performance Analysis](#2-experiment-1---hypervisor-performance-analysis)
3. [Experiment 2 - Online Food Delivery Microservices](#3-experiment-2---online-food-delivery-microservices)
4. [Microservices Architecture](#4-microservices-architecture)
5. [Docker Deployment](#5-docker-deployment)
6. [Inter-Service Communication](#6-inter-service-communication)
7. [Workload Testing](#7-workload-testing)
8. [Performance Results](#8-performance-results)
9. [Analysis](#9-analysis)
10. [Repository Structure](#10-repository-structure)
11. [How to Run the Microservices Application](#11-how-to-run-the-microservices-application)
12. [Conclusion](#12-conclusion)

---

# 1. Repository Overview

This repository contains Cloud Computing laboratory experiments involving:

- Virtualization and hypervisors
- Type-1 and Type-2 hypervisor performance comparison
- Docker containers
- Docker Compose
- Microservice architecture
- Inter-service communication
- Workload testing
- Performance monitoring
- CPU and memory analysis

The experiments demonstrate concepts related to virtualization,
containerization, distributed services, deployment, and performance analysis.

---

# 2. Experiment 1 - Hypervisor Performance Analysis

## Title

**Performance Analysis of Type-1 and Type-2 Hypervisors**

## Objective

The objective of this experiment is to compare the performance of:

- **Type-1 Hypervisor:** Proxmox VE
- **Type-2 Hypervisor:** VMware Workstation

Identically configured Ubuntu Virtual Machines were used for the comparison.

The benchmark was performed using the `sysbench` CPU benchmark.

## Virtual Machine Configuration

| Resource | Proxmox VE | VMware Workstation |
|---|---|---|
| Hypervisor Type | Type-1 / Bare-Metal | Type-2 / Hosted |
| Guest OS | Ubuntu | Ubuntu |
| CPU | 2 vCPU | 2 vCPU |
| RAM | 2 GB | 2 GB |
| Disk | 20 GB | 20 GB |
| Benchmark | Sysbench CPU | Sysbench CPU |
| CPU Benchmark Limit | 20,000 Primes | 20,000 Primes |

## Architecture

### Type-1 Hypervisor

```text
Physical Hardware
       |
       v
Proxmox VE / KVM
       |
       v
Ubuntu Virtual Machine
       |
       v
Sysbench CPU Benchmark
Type-2 Hypervisor
Physical Hardware
       |
       v
Host Operating System
       |
       v
VMware Workstation
       |
       v
Ubuntu Virtual Machine
       |
       v
Sysbench CPU Benchmark
Performance Result
Performance Metric	Proxmox VE	VMware Workstation
Total Execution Time	10.0004 s	10.0007 s
Total Events	17,169	13,650
Events per Second	1,716.69	1,364.78
Minimum Latency	0.57 ms	0.67 ms
Average Latency	0.58 ms	0.73 ms
95th Percentile Latency	0.65 ms	0.89 ms
Maximum Latency	2.78 ms	4.06 ms
Observation

The experiment showed that Proxmox VE achieved higher CPU throughput
and lower latency than VMware Workstation for the tested CPU workload.

The measured throughput advantage of Proxmox VE was approximately 25.79%.

3. Experiment 2 - Online Food Delivery Microservices
Title

Build, Deploy and Analyze a Containerized Microservice Application Under Varying Workloads

Application Domain

Online Food Delivery / Online Food Ordering System

Objective

The objective of this experiment is to design, develop, containerize,
deploy, and analyze an application consisting of independent microservices.

The application demonstrates:

Microservice architecture
REST APIs
Docker containerization
Docker Compose
Inter-service communication
Workload testing
CPU and memory monitoring
Performance analysis under different concurrency levels
Microservices

The application contains exactly three independent microservices.

1. User Service

Responsibility:

Manages user information.

Port:

5001

REST API:

GET /user/<user_id>

Example:

http://localhost:5001/user/1

Example response:

{
    "user_id": 1,
    "name": "Soumya",
    "status": "Active"
}
2. Food Service

Responsibility:

Provides food item information.

Port:

5002

REST API:

GET /food/<food_id>

Example:

http://localhost:5002/food/1

Example response:

{
    "food_id": 1,
    "food": "Pizza",
    "price": 250
}
3. Order Service

Responsibility:

Creates an order by communicating with the User Service
and Food Service.

Port:

5000

REST API:

GET /order/<user_id>/<food_id>

Example:

http://localhost:5000/order/1/1

The Order Service requests user information from the User Service
and food information from the Food Service before creating the order response.

4. Microservices Architecture

The application follows the following architecture:

                     Client
                       |
                       v
              +----------------+
              | Order Service  |
              |    Port 5000   |
              +----------------+
                    /     \
                   /       \
                  v         v
        +---------------+  +---------------+
        | User Service  |  | Food Service  |
        |   Port 5001   |  |   Port 5002   |
        +---------------+  +---------------+
Request Flow
Client
  |
  | GET /order/1/1
  v
Order Service
  |
  |----> User Service
  |       |
  |       └── User details
  |
  |----> Food Service
          |
          └── Food details
  |
  v
Order Created Successfully
5. Docker Deployment

Each microservice has its own Dockerfile.

User Service
    |
    └── Dockerfile

Food Service
    |
    └── Dockerfile

Order Service
    |
    └── Dockerfile

Docker Compose is used to deploy all three services together.

The services communicate using a Docker bridge network:

app-network

The service names are used for communication between containers.

For example:

http://user-service:5001
http://food-service:5002

and:

http://food-service:5002

This allows the Order Service to communicate with the other services
without using localhost inside the Docker network.

Docker Compose Services
order-service
user-service
food-service
Port Mapping
Service	Container Port	Host Port
Order Service	5000	5000
User Service	5001	5001
Food Service	5002	5002
6. Inter-Service Communication

The Order Service communicates with the User Service and Food Service
using HTTP REST requests.

Inside Docker Compose, service names are used as hostnames.

Order Service
      |
      +------> user-service:5001
      |
      +------> food-service:5002

Communication was tested from inside the Order Service container.

Example:

User Service response:
{'name': 'Soumya', 'status': 'Active', 'user_id': 1}

Food Service response:
{'food': 'Pizza', 'price': 250, 'food_id': 1}

The successful response confirms that the microservices can communicate
through the Docker network.

7. Workload Testing

A Python workload testing program was developed using:

Python
Requests
ThreadPoolExecutor

The following concurrency levels were tested:

1
2
4
8
16

Each test used:

20 total requests

The following metrics were recorded:

Average response time
Throughput
Failed requests
CPU utilization
Memory utilization

The workload testing scripts are:

load_test.py
monitor_test.py
8. Performance Results

The following results were obtained during the workload testing experiment.

Concurrency	Avg Response Time (s)	Throughput (req/s)	Failed Requests	Order CPU (%)	Order Memory (MiB)
1	0.0096	8.81	0	3.93	30.03
2	0.0138	10.13	0	0.02	30.36
4	0.0223	9.87	0	0.02	30.08
8	0.0336	9.90	0	0.02	30.06
16	0.0485	9.89	0	0.08	30.12
Other Microservices
User Service
Concurrency	CPU (%)	Memory (MiB)
1	1.24	25.15
2	0.01	25.18
4	0.02	25.17
8	0.02	25.17
16	0.03	25.18
Food Service
Concurrency	CPU (%)	Memory (MiB)
1	0.02	25.11
2	0.02	25.20
4	0.02	25.13
8	0.02	25.18
16	0.03	25.14
9. Analysis
Response Time

As concurrency increased from 1 to 16, the average response time increased:

0.0096 s  →  0.0485 s

This shows that higher concurrent workload resulted in increased response time.

Throughput

Throughput increased initially and then remained approximately stable:

8.81 req/s
10.13 req/s
9.87 req/s
9.90 req/s
9.89 req/s

The system achieved its highest measured throughput at concurrency 2.

After that, throughput remained close to 10 requests per second
under the tested workload and monitoring setup.

Failed Requests

All tested concurrency levels produced:

0 failed requests

This indicates that all 20 requests at each tested concurrency level
were successfully completed.

CPU Utilization

CPU utilization remained low during the workload.

The Order Service showed the highest measured CPU activity among
the three services at some test levels.

Memory Utilization

Memory usage remained almost constant as concurrency increased.

The Order Service used approximately:

30 MiB

while the User Service and Food Service used approximately:

25 MiB

during the tests.

Overall Observation

The application successfully handled the tested workloads without
request failures.

Increasing concurrency increased response time, while throughput
remained relatively stable after the initial increase.

10. Repository Structure

The current repository is organized as follows:

Cloud_computing/
│
├── README.md
├── LAB_REPORT.md
│
├── images/
│   └── Existing experiment screenshots and graphs
│
├── scripts/
│   └── Existing experiment scripts
│
├── vm-vs-container/
│   └── Existing virtualization-related experiment files
│
└── online-food-microservices/
    │
    ├── docker-compose.yml
    ├── load_test.py
    ├── monitor_test.py
    │
    ├── order-service/
    │   ├── app.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── user-service/
    │   ├── app.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    └── food-service/
        ├── app.py
        ├── Dockerfile
        └── requirements.txt
11. How to Run the Microservices Application
Step 1: Open the project directory
cd online-food-microservices
Step 2: Build the Docker images
docker compose build
Step 3: Start all services
docker compose up -d
Step 4: Check running containers
docker ps

The following three services should be running:

order-service
user-service
food-service
Step 5: Test the services
User Service

Open:

http://localhost:5001/user/1
Food Service

Open:

http://localhost:5002/food/1
Order Service

Open:

http://localhost:5000/order/1/1

The Order Service should return a successful order response containing
the user and food information.

Step 6: Run Workload Test

From the online-food-microservices directory:

python load_test.py

For CPU and memory monitoring:

python monitor_test.py
Step 7: Stop the Containers
docker compose down
12. Conclusion

This Cloud Computing laboratory work demonstrates two important areas
of cloud infrastructure and deployment.

The first experiment compares the performance of Type-1 and Type-2
hypervisors using identical Ubuntu virtual machines and a CPU benchmark.

The second experiment demonstrates a containerized microservice
application for an Online Food Delivery system.

The Online Food Delivery application consists of three independent
services:

User Service
Food Service
Order Service

Docker and Docker Compose were used to containerize and deploy the
services. The services communicated through a Docker bridge network
using service names.

Workload testing was performed at five concurrency levels:

1, 2, 4, 8, 16

The application successfully completed all tested requests with
zero failures. Response time increased with concurrency, while
throughput remained relatively stable after the initial increase.
CPU and memory utilization remained low and memory usage remained
nearly constant.

Overall, the experiments demonstrate concepts of:

Virtualization
Hypervisors
Containerization
Microservices
Docker
Docker Compose
REST APIs
Inter-service communication
Workload testing
Resource monitoring
Performance analysis

Laboratory Experiment conducted for Cloud Computing / Computer Networks Course.