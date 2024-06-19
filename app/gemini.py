import google.generativeai as genai
import os


genai.configure(api_key=os.getenv('API_KEY'))

msg = ""

model = genai.GenerativeModel(model_name='gemini-1.5-flash')
response = model.generate_content(
    f"""Please paraphrase this message, do make sure to use emojis
        but less, remove all names and dates in message but keep
        the bitnode same and lastly dont use yearly word too: {msg}""")

print(response.text)
