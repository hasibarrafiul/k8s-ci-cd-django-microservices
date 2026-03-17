import json
import os
import pika


def publish_user_created(user):
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host)
    )
    channel = connection.channel()

    channel.queue_declare(queue="user_created", durable=True)

    message = {
        "event": "USER_CREATED",
        "data": {
            "auth_id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }

    channel.basic_publish(
        exchange="",
        routing_key="user_created",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()