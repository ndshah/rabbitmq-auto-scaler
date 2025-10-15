import yaml
import requests
import subprocess
import time

with open("config.yaml") as f:
    config = yaml.safe_load(f)

RABBITMQ = config['rabbitmq']
CONSUMERS = config['consumers']
POLL_INTERVAL = config.get('poll_interval', 5)

running_consumers = {c['name']: [] for c in CONSUMERS}

def get_queue_length(queue_name):
    url = f"http://{RABBITMQ['host']}:{RABBITMQ['port']}/api/queues/{RABBITMQ['vhost'].replace('/', '%2F')}/{queue_name}"
    resp = requests.get(url, auth=(RABBITMQ['username'], RABBITMQ['password']))
    if resp.status_code == 200:
        data = resp.json()
        return data['messages_ready']
    return 0

while True:
    for consumer in CONSUMERS:
        queue = consumer['queue']
        name = consumer['name']
        min_inst = consumer['min_instances']
        max_inst = consumer['max_instances']
        up_thr = consumer['scale_up_threshold']
        down_thr = consumer['scale_down_threshold']

        queue_len = get_queue_length(queue)
        current_instances = len(running_consumers[name])

        # Scale up
        if queue_len > up_thr and current_instances < max_inst:
            p = subprocess.Popen(['python3.11', consumer['script'], name])
            running_consumers[name].append(p)
            print(f"[{name}] Queue={queue_len}, Scaling UP. New instances={len(running_consumers[name])}")

        # Scale down
        elif queue_len < down_thr and current_instances > min_inst:
            proc = running_consumers[name].pop()
            proc.terminate()
            print(f"[{name}] Queue={queue_len}, Scaling DOWN. New instances={len(running_consumers[name])}")

    time.sleep(POLL_INTERVAL)
