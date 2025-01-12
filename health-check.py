import requests
import time
import signal
import sys
import yaml
import argparse
from urllib.parse import urlparse

# Load domains and configurations from sample.yaml
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Dictionary to keep track of health check results
health_check_results = {}

def signal_handler(sig, frame):
    print("\nUser pressed CTRL+C. Exiting the program.")
    log_availability()
    sys.exit(0)

def log_availability():
    print("\nLogging availability percentages:")
    domain_results = {}
    for url, results in health_check_results.items():
        domain = urlparse(url).netloc
        if domain not in domain_results:
            domain_results[domain] = {"up": 0, "down": 0}
        domain_results[domain]["up"] += results["up"]
        domain_results[domain]["down"] += results["down"]

    for domain, results in domain_results.items():
        total_checks = results["up"] + results["down"]
        if total_checks > 0:
            availability_percentage = (results["up"] / total_checks) * 100
            print(f"{domain} has {round(availability_percentage)}% availability percentage")
        else:
            print(f"{domain} has no checks performed")

def check_health(config):
    url = config.get('url')
    method = config.get('method', 'GET')
    headers = config.get('headers', {})
    body = config.get('body', None)

    if url not in health_check_results:
        health_check_results[url] = {"up": 0, "down": 0}

    try:
        start_time = time.time()
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=body)
        else:
            print(f"Unsupported method {method} for URL {url}")
            return
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        if 200 <= response.status_code < 300 and latency < 500:
            health_check_results[url]["up"] += 1
            print(f"{url} is UP (status code: {response.status_code}, latency: {latency} ms)")
        else:
            health_check_results[url]["down"] += 1
            print(f"{url} is DOWN (status code: {response.status_code}, latency: {latency} ms)")
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")
        health_check_results[url]["down"] += 1

def main():
    parser = argparse.ArgumentParser(description="Health check script")
    parser.add_argument("config_file", help="Path to the configuration YAML file")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    print("Starting health checks. Press CTRL+C to stop.")

    configs = load_config(args.config_file)
    print(f"Loaded configurations for {len(configs)} endpoints.")

    while True:
        for config in configs:
            print(f"Checking health for {config.get('url')}")
            check_health(config)
        log_availability()
        time.sleep(15)  # Wait for 15 seconds before the next check

if __name__ == "__main__":
    main()