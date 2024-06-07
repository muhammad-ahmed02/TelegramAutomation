import google.generativeai as genai
import os


genai.configure(api_key=os.getenv('API_KEY'))

msg = "Yearly Exclusive\
Coin Name: ENJ\
Entry Position: Long\
Coin Value: 0.3413\
Date and Time: 2024-05-31-21-54-42\
Note: Manage your risk\
any trade can fail. Bitnode cordinate 7350'12"

model = genai.GenerativeModel(model_name='gemini-1.5-flash')
response = model.generate_content(
    f"""Please paraphrase this message, do make sure to use emojis
    but less and dont change the coin name: {msg}""")

print(response.text)
