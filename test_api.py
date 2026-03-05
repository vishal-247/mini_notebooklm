from groq import Groq
from dotenv import load_dotenv
import os   

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "Hello"}
    ],
    model="openai/gpt-oss-120b",
)

print(chat_completion.choices[0].message.content)
print(client.models.list())