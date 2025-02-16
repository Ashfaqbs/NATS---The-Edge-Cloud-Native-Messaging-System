import asyncio
from nats.aio.client import Client as NATS

async def run_publisher():
    nc = NATS()
    await nc.connect("localhost:4222")
    
    # Obtain a JetStream context
    js = nc.jetstream()

    msg_count = 0
    while True:
        msg_count += 1
        message = f"Message {msg_count}"
        # Publish message to subject "mymessages"
        ack = await js.publish("mymessages", message.encode())
        print(f"Published: {message} (Ack: {ack})")
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(run_publisher())
