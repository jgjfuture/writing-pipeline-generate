import os
import json
from src import gpt_generate


def main():
    api_key = os.getenv('OPENAI_API_KEY')
    messages, function = gpt_generate.generate_message_query_prompt(
        "書き出す\n5min\n- あしたの天気はあれらしいです？\n_どうにかじて騎麗なテキストを生成したい〇")
    chat_response = gpt_generate.gpt_generate(messages, [function], api_key, function['name'])
    if chat_response.choices[0].finish_reason != "stop":
        print("ChatGPT did not finish generating text")
        return
    generated_text = json.loads(chat_response.choices[0].message.function_call.arguments).get('markdown')
    used_tokens = chat_response.usage.total_tokens
    print("Used tokens: " + str(used_tokens))
    print("Generated text: " + generated_text)

main()
