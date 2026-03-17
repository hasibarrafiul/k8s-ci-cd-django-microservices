import json
import os
import time

import pika
from pika.exceptions import AMQPConnectionError

from user_app.models import User


def callback(ch, method, properties, body):
    try:
        payload = json.loads(body)
        print("Received message:", payload)

        event = payload.get("event")
        data = payload.get("data", {})

        if event == "USER_CREATED":
            auth_id = data.get("auth_id")
            username = data.get("username")
            email = data.get("email")

            if auth_id and username and email:
                User.objects.get_or_create(
                    auth_id=auth_id,
                    defaults={
                        "username": username,
                        "email": email,
                    },
                )
                print(f"User synced: {username}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("Consumer error:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_consumer():
    print("Starting consumer...")

    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
    connection = None

    while connection is None:
        try:
            print(f"Trying to connect to RabbitMQ at {rabbitmq_host}...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbitmq_host)
            )
        except AMQPConnectionError:
            print("RabbitMQ not ready yet, retrying in 5 seconds...")
            time.sleep(5)

    channel = connection.channel()
    channel.queue_declare(queue="user_created", durable=True)
    channel.basic_consume(
        queue="user_created",
        on_message_callback=callback,
    )

    print("Waiting for user_created messages...")
    channel.start_consuming()