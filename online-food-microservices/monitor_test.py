import subprocess
import time
import requests
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:5000/order/1/1"

TOTAL_REQUESTS = 20
CONCURRENCY_LEVELS = [1, 2, 4, 8, 16]

CONTAINERS = [
    "online-food-microservices-order-service-1",
    "online-food-microservices-user-service-1",
    "online-food-microservices-food-service-1"
]


def send_request():
    try:
        start = time.time()
        response = requests.get(URL)
        end = time.time()

        return end - start, response.status_code == 200

    except Exception:
        return 0, False


def get_docker_stats():

    result = subprocess.run(
        ["docker", "stats", "--no-stream",
         "--format",
         "{{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}"],
        capture_output=True,
        text=True
    )

    stats = {}

    for line in result.stdout.strip().splitlines():

        parts = line.split(",")

        if len(parts) >= 4:
            name = parts[0]
            cpu = parts[1]
            memory = parts[2]
            mem_percent = parts[3]

            stats[name] = {
                "cpu": cpu,
                "memory": memory,
                "memory_percent": mem_percent
            }

    return stats


for concurrency in CONCURRENCY_LEVELS:

    print("\n======================================")
    print("Concurrency:", concurrency)
    print("======================================")

    cpu_samples = {
        container: []
        for container in CONTAINERS
    }

    memory_samples = {
        container: []
        for container in CONTAINERS
    }

    # Start workload
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:

        futures = [
            executor.submit(send_request)
            for _ in range(TOTAL_REQUESTS)
        ]

        # Monitor Docker while requests are running
        while not all(future.done() for future in futures):

            stats = get_docker_stats()

            for container in CONTAINERS:

                if container in stats:

                    cpu_value = float(
                        stats[container]["cpu"].replace("%", "")
                    )

                    memory_value = float(
                        stats[container]["memory"].split("/")[0]
                        .replace("MiB", "")
                        .replace("GiB", "")
                        .strip()
                    )

                    cpu_samples[container].append(cpu_value)
                    memory_samples[container].append(memory_value)

            time.sleep(0.1)

    total_time = time.time() - start_time

    results = [future.result() for future in futures]

    successful = sum(1 for r in results if r[1])
    failed = TOTAL_REQUESTS - successful

    response_times = [r[0] for r in results]

    average_response_time = (
        sum(response_times) / len(response_times)
    )

    throughput = successful / total_time

    print("Successful Requests:", successful)
    print("Failed Requests:", failed)
    print(
        "Average Response Time:",
        round(average_response_time, 4),
        "seconds"
    )
    print(
        "Throughput:",
        round(throughput, 2),
        "requests/second"
    )

    print("\nCPU and Memory:")

    for container in CONTAINERS:

        if cpu_samples[container]:

            average_cpu = (
                sum(cpu_samples[container])
                / len(cpu_samples[container])
            )

            average_memory = (
                sum(memory_samples[container])
                / len(memory_samples[container])
            )

            print("\n", container)
            print(
                "Average CPU:",
                round(average_cpu, 3),
                "%"
            )
            print(
                "Average Memory:",
                round(average_memory, 2),
                "MiB"
            )