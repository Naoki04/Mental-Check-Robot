import pyaudio
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
import time
import datetime
from tqdm import tqdm
import pygame.mixer
from mutagen.mp3 import MP3
import cv2

from google.cloud import vision
import io   

def record(idx, sr, framesize, t):
    pa = pyaudio.PyAudio() # PyAudioインスタンスの作成
    data = [] # 音声データが入る入れ物
    dt = 1 / sr # 1サンプルの秒数

    # ストリームの開始
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=sr,
                     input=True, input_device_index=idx, frames_per_buffer=framesize)
    
    # フレームサイズ毎に音声を録音
    for i in tqdm(range(int(((t / dt) / framesize)))): # t/dtでdtが繰り返される数。それをframesizeで割ることでフレーム単位の処理が何回行われるかを数えている。
        frame = stream.read(framesize) # 録音を読み取る部分
        data.append(frame) # 入れ物に格納する部分
    
    # ストリームの終了
    stream.stop_stream() # 然るべき回数繰り返された後は終了。
    stream.close()
    pa.terminate()
    
    # フレームごとのデータをまとめる処理
    data = b"".join(data)

    # データをNumpy配列に変換
    data = np.frombuffer(data, dtype="int16")
    # pyaudio.paInt16で量子化しているため「2^(16-1)-1」で正規化している
    data_show = np.frombuffer(data, dtype="int16") / float((np.power(2, 16) / 2) - 1)

    filename = "data/record/"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".wav"
    write(filename, sr, data)

    return filename #data, data_show, i


def play(filename):
    # Check length
    audio = MP3(filename)
    length = audio.info.length

    # mixerモジュールの初期化
    pygame.mixer.init()
    # 音楽ファイルの読み込み
    pygame.mixer.music.load(filename)
    # 音楽再生、および再生回数の設定(-1はループ再生)
    pygame.mixer.music.play(1)
    time.sleep(length)
    # 再生の終了
    pygame.mixer.music.stop()




def texttospeech(text):
    # [START tts_quickstart]
    """Synthesizes speech from the input string of text or ssml.
 
    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """

    from google.cloud import texttospeech
    
 
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
 
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)
 
    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
 
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
 
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    filename = "data/speech/"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".mp3"
    # The response's audio_content is binary.
    with open(filename, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        #print('Audio content written to file "')
    # [END tts_quickstart]

    return filename

def capture_image(cap):
    #カメラからの画像取得
    ret, frame = cap.read()

    filename = "data/face/"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".jpg"
    cv2.imwrite(filename, frame)

    return filename

def emotion_recognition(filename):
    
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(filename, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    """
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    """
    likelihood_name = ('0', '0', '1', '2',
                       '3', '4')
    print('Faces:')

    for face in faces:
        #print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        #print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))
        #print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        #print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        #print('face bounds: {}'.format(','.join(vertices)))
    return {"joy":likelihood_name[face.joy_likelihood], "sorrow":likelihood_name[face.sorrow_likelihood], "anger":likelihood_name[face.anger_likelihood], "surprise":likelihood_name[face.surprise_likelihood]}



    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))



def main():
    sr = 44100        # サンプリングレート
    framesize = 1024  # フレームサイズ
    idx = 0           # マイクのチャンネル
    t = 4             # 計測時間[s]

    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        print(pa.get_device_info_by_index(i))
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("START")

    data, data_show, i = record(idx, sr, framesize, t)
    """
    t = np.arange(0, framesize * (i+1) * (1 / sr), 1 / sr)
    plt.plot(t, wfm, label='signal')
    plt.show()
    """
    write("data/audio_record.wav", sr, data)



if __name__ == "__main__":
    main()