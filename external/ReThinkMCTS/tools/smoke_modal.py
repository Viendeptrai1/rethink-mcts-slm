import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    base_url=os.environ["MODAL_BASE_URL"],
    api_key=f"{os.environ['MODAL_PROXY_TOKEN_ID']}.{os.environ['MODAL_PROXY_TOKEN_SECRET']}",
)

completion = client.chat.completions.create(
    model=os.environ["KIMI_MODEL"],
    messages=[
        {"role": "system", "content": "You are a concise technical assistant."},
        {"role": "user", "content": "1 + 1 = "},
    ],
    temperature=0.3,
    max_tokens=2048,
    top_p=0.95,
    stream=False,
    extra_body={"reasoning_effort": "xhigh"},
)
print(completion.choices[0].message.content)
