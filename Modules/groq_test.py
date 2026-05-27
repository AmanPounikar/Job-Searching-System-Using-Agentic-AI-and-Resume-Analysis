import os
from dotenv import load_dotenv
from groq import Groq

# load env
load_dotenv(dotenv_path="C:/Codes/Project main folder/.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say hello in one line"}]
    )

    print("✅ GROQ WORKING")
    print("Response:", response.choices[0].message.content)

except Exception as e:
    print("❌ ERROR:", e)