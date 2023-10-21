import os
from src import gpt_generate
from src import format


def main():
    api_key = os.getenv('OPENAI_API_KEY')
    messages = gpt_generate.generate_message_query_prompt(
        "書き出す\n5min\n- あしたの天気はあれらしいです？\n_どうにかじて騎麗なテキストを生成したい〇")
    chat_response = gpt_generate.gpt_generate(messages, api_key)
    if chat_response.choices[0].finish_reason != "stop":
        print("ChatGPT did not finish generating text")
        return
    generated_text = chat_response.choices[0].message.content
    formatted_text = format.extract_code_blocks(
        generated_text) or generated_text
    used_tokens = chat_response.usage.total_tokens
    print("Used tokens: " + str(used_tokens))
    print("Generated text: " + formatted_text)


main()
