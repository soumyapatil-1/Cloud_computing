import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:5000/order/1/1"

TOTAL_REQUESTS = 20

CONCURRENCY_LEVELS = [1, 2, 4, 8, 16]


def send_request():
    start = time.time()

    try:
        response = requests.get(URL)
        end = time.time()

        if response.status_code == 200:
            return end - start, True
        else:
            return end - start, False

    except Exception:
        end = time.time()
        return end - start, False


for concurrency in CONCURRENCY_LEVELS:

    print("\n======================================")
    print("Concurrency:", concurrency)
    print("======================================")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(
            executor.map(
                lambda x: send_request(),
                range(TOTAL_REQUESTS)
            )
        )

    total_time = time.time() - start_time

    response_times = [r[0] for r in results]
    successful = sum(1 for r in results if r[1])
    failed = TOTAL_REQUESTS - successful

    average_response_time = sum(response_times) / len(response_times)

    throughput = successful / total_time

    print("Total Requests:", TOTAL_REQUESTS)
    print("Successful Requests:", successful)
    print("Failed Requests:", failed)
    print("Average Response Time:", round(average_response_time, 4), "seconds")
    print("Throughput:", round(throughput, 2), "requests/second")