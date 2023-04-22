import apiFunctions as api
import pyaudio
from scipy.io.wavfile import write
import time
import yaml
import warnings

import whisper
import openai


"""
Settings
"""
sr = 44100        # サンプリングレート
framesize = 1024  # フレームサイズ
idx = 0           # マイクのチャンネル
t = 10             # 計測時間[s]

warnings.simplefilter('ignore')


"""
Variables
"""
messages = [
    {
        "role": "system",
        "content": "You are a professional clinical psychologist who is friendly and like short conversations."
    },
    {
        "role": "assistant",
        "content": "Today let's talk about your daily life like daily conversation."
    },
    {
        "role": "assistant",
        "content": "Hello, I'm David, how are you doing today?"
    },
]


def initialize():
    print("Initializing...")
    # Initializing PyAudio
    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        pa.get_device_info_by_index(i)

    # Initializing Whisper
    whisper_model = whisper.load_model("base.en")

    # Initializing ChatGPT
    with open('settings.yaml', 'r') as f:
        settings = yaml.load(f)
    openai.api_key = settings["openai-key"]
    
    return pa, whisper_model



def main():
    pa, whisper_model = initialize()
    print("Hello, I'm David, how are you doing today?")
    while True:
        time.sleep(5)
        # Count down
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("===START===")

        # Record
        filename = api.record(idx, sr, framesize, t)
        print("Saved to", filename)

        # Audio -> Text
        result = whisper_model.transcribe(filename)
        print(result["text"])

        # Text -> ChatGPT -> Text
        print("------------")
        messages.append(
            {
                "role": "user",
                "content": result["text"]
            }
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response['choices'][0]['message']['content']
        print(reply)

        # Save reply to messages[]
        messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )


if __name__ == "__main__":
    main()



import openai
import yaml

# Load settings


