# !pip install openai

import openai
import yaml

# Load settings
with open('settings.yaml', 'r') as f:
    settings = yaml.load(f)
    #print(settings)

openai.api_key = settings["openai-key"]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
             "role": "system",
             "content": "You are a professional clinical psychologist who is friendly and like short conversations."
         },
         {
             "role": "assistant",
             "content": "Today let's talk about your daily life like daily conversation."
         },
        {
            "role": "user", 
            "content": "I feel depressed these days."
        }
    ]
)

print(response['choices'][0]['message']['content'])