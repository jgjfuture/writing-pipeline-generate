import openai


def gpt_generate(messages_array, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_array
    )
    return response


def generate_message_query_prompt(reasoning_text):
    messages = [
        {
            "role": "user",
            "content": "今から、OCRで取得した、ちょっと読みにくく、誤字があり、文書の区切りが不自然であるような文書を渡すので、元の内容の復元を試みて報告してください。自然でない日本語は自然に直しておいてください。"
        },
        {
            "role": "assistant",
            "content": "はい、わかりました。元の文章に関してわかっていることはありますか？"
        },
        {
            "role": "user",
            "content": "はい、あります。推測のヒントをお伝えします。1. 文書は箇条書きです。 2. 1項目が1行に記されているとは限らず、1項目が複数行に及んでいる可能性もあります。箇条書きの点がOCRで読み取れているとは限らないので、うまく文書を区切ったりまとめたりする必要があるかもしれません。 3. 箇条書きの1項目は1つの文で構成されています。 4. 速記しているため、ひらがなが多く、誤字があることもあります。漢字への変換にミスがあるかもしれません。文章にミスがあると感じたら修正して私が書こうとした内容を復元してください。 5. 文章の1行目は文書のタイトルであることが多いです。これは無視してください。"
        },
        {
            "role": "assistant",
            "content": "ありがとうございます。では、どのようにお伝えすればいいですか？提示された形式でお伝えします。"
        },
        {
            "role": "user",
            "content": "推測した文書をそのまま提示するのではなく、その内容をMarkdownの箇条書きにしてください。通常の項目は順序付きの箇条書きではなく、順序なしの箇条書きで表現してください。また、箇条書きの項目の内容がTODOとして判断できるとあなたが解釈したなら、Markdownのチェックリストで表現してください。`- [ ]`で表現されるものです。マークダウンのコードブロックに入れてコードを提出してください。"
        },
        {
            "role": "assistant",
            "content": "わかりました。では、文章をお預かりします。"
        },
        {
            "role": "user",
            "content": reasoning_text
        }
    ]
    return messages

def generate_title_query_prompt(message):
    messages = [
        {
            "role": "user",
            "content": "今から箇条書きで構成された文書を渡すので、そのタイトルを推測してください。結果としてタイトルのみを出力してください。"
        },
        {
            "role": "assistant",
            "content": "はい、わかりました。では文書を頂戴します。"
        },
        {
            "role": "user",
            "content": message
        },
    ]
    return messages

def generate_comment_query_prompt(title, message):
    messages = [
        {
            "role": "system",
            "content": "あなたはアドバイザーです。あなたはクライアントが記述した日記に目を通して、メンタルヘルスあるいは健康の観点からよりよい人生が歩めるようにアドバイスを行います。あなたはメンタルヘルスや健康に関する専門家です。あなたは書いてある内容自体に対するコメントに加えて、その内容を記述したこと自体にも触れてください。"
        },
        {
            "role": "user",
            "content": "今から、タイトルと箇条書きで構成された日記を渡すので、その内容についてあなたの意見に基づくコメントをしてください。コメントは十分に長く、できるだけ文章のすべての項目にください。"
        },
        {
            "role": "assistant",
            "content": "はい、わかりました。では日記を見せてもらいますね。"
        },
        {
            "role": "user",
            "content": "タイトル: ${title}\n文書: ${message}"
        }
    ]
    return messages