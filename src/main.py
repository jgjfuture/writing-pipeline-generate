import base64
import functions_framework
import os
import gpt_generate
import publish
import json


@functions_framework.cloud_event
def entry_point(cloud_event):
    api_key = os.getenv('OPENAI_API_KEY')
    pubsub_topic_name = os.getenv('PUBSUB_TOPIC_NAME')
    data = base64.b64decode(cloud_event.data["message"]["data"])
    data = data.decode("utf-8")
    data = json.loads(data)
    page_id = data["notionPageId"]
    reasoning_text = data["reasoningText"]
    messages, function = gpt_generate.generate_message_query_prompt(reasoning_text)
    chat_response = gpt_generate.gpt_generate(messages, [function], api_key, function['name'])
    generated_text = extract_ai_response(chat_response)
    if not generated_text:
        print("ChatGPT did not finish generating text")
        return

    extracted_markdown = json.loads(generated_text.arguments).get('markdown')
    extracted_title = json.loads(generated_text.arguments).get('title')

    messages, function = gpt_generate.generate_comment_query_prompt(extracted_markdown, extracted_title)
    chat_response = gpt_generate.gpt_generate(messages, [function], api_key, function['name'])
    generated_comment = extract_ai_response(chat_response)
    if not generated_comment:
        print("ChatGPT did not finish generating text")
        return

    comment = json.loads(generated_comment.arguments).get('comment')

    used_tokens = chat_response.usage.total_tokens
    publish.publish_message(publish.makePublishMessage(page_id, extracted_markdown, extracted_title, comment), pubsub_topic_name)

def extract_ai_response(chat_response):
    if chat_response.choices[0].finish_reason != "stop":
        print("ChatGPT did not finish generating text")
        return False
    return chat_response.choices[0].message.function_call