import openai


def gpt_generate(messages_array, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_array
    )
    return response


def generate_messages(reasoning_text):
    messages = [
        {
            "role": "system",
            "content": "あなたは秘書です。私のために書類のチェックやタスクの整理などを行います。"
        },
        {
            "role": "user",
            "content": "今から、OCRで取得した、ちょっと読みにくく、誤字があり、文書の区切りが不自然であるような文書を渡すので、元の内容の復元を試みて報告してください。元の文章についてわかっていることをお伝えします。1. 文書は箇条書きです。 2. 1項目が1行に記されているとは限らず、1項目が複数行に及んでいる可能性もあります。箇条書きの点がOCRで読み取れているとは限らないので、うまく文書を区切ったりまとめたりする必要があるかもしれません。 3. 箇条書きの1項目は1つの文で構成されています。 4. 速記しているため、ひらがなが多く、誤字があることもあります。元の文書の復元というより、私が書こうとしていたことを推測することになります。 報告のフォーマットについてお知らせします。内容のトピックや内容に応じて分類してから報告してください。何か実行するべきことが示唆されている場合は、それも抜き出して報告してください。最後に、その内容をMarkdownの正式な書式に乗っ取ったMarkdown文書として提出してください。通常の項目は順序付きの箇条書きではなく、順序なしの箇条書きで表現してください。また、実行するべきことはMarkdownのチェックリストで表現してください。`- [ ]`で表現されるものです。出力は、Markdown文書のみで構いません。"
        },
        {
            "role": "assistant",
            "content": "はい、わかりました。文章をお預かりします。"
        },
        {
            "role": "user",
            "content": reasoning_text
        }
    ]
    return messages
