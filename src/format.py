import re

def extract_code_blocks(text):
    pattern = r"```(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    block_inner = matches[0] if matches else False
    if not block_inner:
        return False
    # Remove first line "markdown" if present
    pure_text = re.sub(r"^markdown\n", "", block_inner, flags=re.IGNORECASE)
    return pure_text

def extract_title(title):
    pattern = r"「(.*?)」"
    matches = re.findall(pattern, title, re.DOTALL)
    title = matches[0] if matches else title
    pattern = r"\"(.*?)\""
    matches = re.findall(pattern, title, re.DOTALL)
    return matches[0] if matches else title