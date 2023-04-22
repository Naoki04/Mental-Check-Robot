import pyaudio
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
import time
import datetime
from tqdm import tqdm

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

    filename = "data/"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".wav"
    write(filename, sr, data)

    return filename #data, data_show, i


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