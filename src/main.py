import base64
import functions_framework
import os
import gpt_generate
import publish
import format
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
    messages = gpt_generate.generate_message_query_prompt(reasoning_text)
    chat_response = gpt_generate.gpt_generate(messages, api_key)
    generated_text = extract_ai_response(chat_response)
    if not generated_text:
        print("ChatGPT did not finish generating text")
        return

    messages = gpt_generate.generate_title_query_prompt(generated_text)
    chat_response = gpt_generate.gpt_generate(messages, api_key)
    generated_title = extract_ai_response(chat_response)
    if not generated_title:
        print("ChatGPT did not finish generating text")
        return

    messages = gpt_generate.generate_comment_query_prompt(generated_title, generated_text)
    chat_response = gpt_generate.gpt_generate(messages, api_key)
    generated_comment = extract_ai_response(chat_response)
    if not generated_comment:
        print("ChatGPT did not finish generating text")
        return

    formatted_text = format.extract_code_blocks(generated_text) or generated_text
    formatted_title = format.extract_title(generated_title)
    used_tokens = chat_response.usage.total_tokens
    print("Used tokens: " + str(used_tokens))
    print("Generated text: " + formatted_text)
    publish.publish_message(publish.makePublishMessage(page_id, formatted_text, formatted_title, generated_comment), pubsub_topic_name)

def extract_ai_response(chat_response):
    if chat_response.choices[0].finish_reason != "stop":
        print("ChatGPT did not finish generating text")
        return False
    return chat_response.choices[0].message.content