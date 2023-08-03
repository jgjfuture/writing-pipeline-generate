import base64
import functions_framework
import os
import gpt_generate
import publish


@functions_framework.cloud_event
def entry_point(cloud_event):
    api_key = os.getenv('OPENAI_API_KEY')
    pubsub_topic_name = os.getenv('PUBSUB_TOPIC_NAME')
    data = base64.b64decode(cloud_event.data["message"]["data"])
    page_id = data["notionPageId"]
    reasoning_text = data["reasoningText"]
    messages = gpt_generate.generate_messages(reasoning_text)
    chat_response = gpt_generate.gpt_generate(messages, api_key)
    if chat_response.choices[0].finish_reason != "stop":
        print("ChatGPT did not finish generating text")
        return
    generated_text = chat_response.choices[0].message.content
    used_tokens = chat_response.usage.total_tokens
    print("Used tokens: " + str(used_tokens))
    publish.publish_message(publish.makePublishMessage(page_id, generated_text), pubsub_topic_name)