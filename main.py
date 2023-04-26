import apiFunctions as api
import pyaudio
from scipy.io.wavfile import write
import time
import yaml
import warnings
import cv2

import whisper
import openai

# Sometimes, Google Login is required.
# !gcloud auth application-default login

"""
Settings
"""
sr = 44100        # サンプリングレート
framesize = 1024  # フレームサイズ
idx = 0           # マイクのチャンネル
t = 12            # 計測時間[s]

device_num = 1

initial_text = "Hello, I'm David. How are you doing today?"
charactor_setting = {
        "role": "system",
        "content": "You are a professional clinical psychologist who is friendly and like short conversations. mainly, he reply only in 3 or 4 sentents in conversation."
    }
warnings.simplefilter('ignore')


"""
Variables
"""
messages = [
    charactor_setting,   
    {
        "role": "assistant",
        "content": "Today let's talk about your daily life like daily conversation."
    },
    {
        "role": "assistant",
        "content": initial_text
    },
]

emotion_array = []


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

    cap = cv2.VideoCapture(device_num)
    
    return pa, whisper_model, cap

def check_topic(messages):
    print("~~Topic/Style CHECK~~")
    recent_messages =  messages[-6:] # extruct last 6 messages
    operation = {
        "role": "user",
        "content": "Can you describe the above conversation in two words, the first describing the topic, the second describing the style in an extremely detailed way of the conversation? Please don't reply any other words besides the two words."
    }
    recent_messages.append(operation)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=recent_messages
    )
    print("Topic/Style:", response['choices'][0]['message']['content'])
    
    return response['choices'][0]['message']['content']
 

def emotion_check(emotion_array): # Using Google Cloud Vision API
    print("~~EMOTION CHECK~~")
    recent_emotions =  emotion_array[-6:] # extruct last 6 emotions
    joy = 0
    sorrow = 0
    anger = 0
    surprise = 0
    n = len(recent_emotions)
    for emotion in recent_emotions:
        joy += int(emotion["joy"])/n
        sorrow += int(emotion["sorrow"])/n
        anger += int(emotion["anger"])/n
        surprise += int(emotion["surprise"])/n
    result = {"joy": joy, "sorrow": sorrow, "anger": anger, "surprise": surprise}
    print(result)

    return result

def emotion_check2(emotion_array): # Using UserLocal's emotion API
    print("~~EMOTION CHECK~~")
    recent_emotions =  emotion_array[-6:] # extruct last 6 emotions
    happy = 0
    sad = 0
    surprise = 0
    anger = 0
    n = len(recent_emotions)
    for emotion in recent_emotions:
        happy += emotion["happy"]/n
        sad += emotion["sad"]/n
        surprise += emotion["surprise"]/n
        anger += emotion["anger"]/n
    result = {"happy": happy, "sad": sad, "surprise": surprise, "anger": anger}
    print(result)

    return result

def topic_control(emotion_array, topic_style):
    if emotion_array["happy"] >= 0.5:
        operation = {
            "role": "system",
            "content": "The user looks like feeling happy in the last six interaction about" + topic_style + ". Please keep the topic and naturally without realized by the user to make the user feeling good."
        }
    elif max(emotion_array.values()) >= 0.2 and max(emotion_array, key=emotion_array.get)!="happy":
        operation = {
            "role": "system",
            "content": "The user looks like feeling " + max(emotion_array, key=emotion_array.get) + " in the last six interaction about" + topic_style + ". Please change the topic to something else naturally without realized by the user."
        }
    else:
        operation = "None"
    print("!Operation!:", operation)
    return operation
        


def main():
    pa, whisper_model, cap = initialize()
    
    # Initial Message
    print(initial_text)
    filename = api.texttospeech(initial_text)
    api.play(filename)
    print("played")

    interactions = 0
    
    while True:
        #time.sleep(7)
        # Count down
        print("3")
        time.sleep(0.5)
        print("2")
        time.sleep(0.5)
        print("1")
        time.sleep(0.5)
        print("===START===")

        # Record
        filename = api.record(idx, sr, framesize, t)
        print("Saved to", filename)

        # Emotion Check2
        image = api.capture_image(cap)
        result_emotion = api.emotion_recognition2(image)
        print(result_emotion)
        emotion_array.append(result_emotion)

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

        # Text -> Audio
        filename = api.texttospeech(reply)
        api.play(filename)

        # Emotion Check2
        image = api.capture_image(cap)
        result_emotion = api.emotion_recognition2(image)
        print(result_emotion)
        emotion_array.append(result_emotion)

        interactions += 1
        

        # Every three interactions...
        if interactions >= 3 and interactions % 3 == 0:
            # Topic check
            topic_style = check_topic(messages)
            # Emotion Check
            current_emotion = emotion_check2(emotion_array)
            # Add Operation
            operation = topic_control(current_emotion, topic_style)
            if operation != "None":
                messages.append(operation)
                messages.append(charactor_setting)

    #メモリを解放して終了するためのコマンド
    cap.release()
    cv2.destroyAllWindows()

    


if __name__ == "__main__":
    main()