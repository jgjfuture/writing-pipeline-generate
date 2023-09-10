from google.cloud import pubsub_v1
import json


def publish_message(message, pubsub_topic_name):
    publisher = pubsub_v1.PublisherClient()
    encoded_message = message.encode("utf-8")
    future = publisher.publish(pubsub_topic_name, encoded_message)
    print(future.result())


def makePublishMessage(page_id, generated_text, generated_title, generated_comment):
    return json.dumps({
        "notionPageId": page_id,
        "generatedText": generated_text,
        "generatedTitle": generated_title,
        "generatedComment": generated_comment
    }, ensure_ascii=False)
