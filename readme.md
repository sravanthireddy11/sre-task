

https://fetch-hiring.s3.us-east-1.amazonaws.com/site-reliability-engineer/health-check.pdf

## Instructions to Run the Code

1. Install Dependencies: Ensure you have requests and pyyaml libraries installed. You can install them using pip:

```bash
python3 -m venv .
source bin/activate
pip3 install requests pyyaml
```

2. Create sample.yaml: Create a sample.yaml file with the following content:

```bash
- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: fetch index page
  url: https://fetch.com/
- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: fetch careers page
  url: https://fetch.com/careers
- body: '{"foo":"bar"}'
  headers:
    content-type: application/json
    user-agent: fetch-synthetic-monitor
  method: POST
  name: fetch some fake post endpoint
  url: https://fetch.com/some/post/endpoint
- name: fetch rewards index page
  url: https://www.fetchrewards.com/
```

3. Run the Script: Execute the script using Python:

```bash
python3 health-check.py sample.yaml

Starting health checks. Press CTRL+C to stop.
Loaded configurations for 4 endpoints.
Checking health for https://fetch.com/
https://fetch.com/ is UP (status code: 200, latency: 53.6808967590332 ms)
Checking health for https://fetch.com/careers
https://fetch.com/careers is UP (status code: 200, latency: 35.25400161743164 ms)
Checking health for https://fetch.com/some/post/endpoint
https://fetch.com/some/post/endpoint is DOWN (status code: 403, latency: 27.576923370361328 ms)
Checking health for https://www.fetchrewards.com/
https://www.fetchrewards.com/ is UP (status code: 200, latency: 95.23868560791016 ms)

Logging availability percentages:
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage
Checking health for https://fetch.com/
https://fetch.com/ is UP (status code: 200, latency: 42.37985610961914 ms)
Checking health for https://fetch.com/careers
https://fetch.com/careers is UP (status code: 200, latency: 35.13383865356445 ms)
Checking health for https://fetch.com/some/post/endpoint
https://fetch.com/some/post/endpoint is DOWN (status code: 403, latency: 27.376174926757812 ms)
Checking health for https://www.fetchrewards.com/
https://www.fetchrewards.com/ is UP (status code: 200, latency: 109.56501960754395 ms)

Logging availability percentages:
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage

```