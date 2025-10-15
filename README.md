# rabbitmq-auto-scaler
Auto Scaler consumer for RabbitMQ in Python

# How to Run the Demo

1. Start RabbitMQ server (and Management UI).

2. Run the auto-scaler:

`python autoscaler.py`

(It will automatically spawn 1 consumer per type initially.)

3. Run the producer:

`python producer.py`

Watch the auto-scaler spawn more consumers if the queue length exceeds thresholds.
Once queues drain, the auto-scaler will scale down instances.

✅ Outcome

- Auto-scaling works per consumer type.
- Queue lengths drive scaling decisions.
- Environment-agnostic and easy to extend for hundreds of queues.
