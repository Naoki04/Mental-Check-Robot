# マルチスレッドがキーボードやマウスが動いてないと止まるバグがある。

## このファイル内にイベントを記述
import tkinter as tk
import threading
import time

import apiFunctions as api


# Demoモード中に別スレッドで実行し続ける関数
def demo_runnnig(button,panel1,panel2):
    panel1.set(0)
    panel2.set(0)
    while(button["text"]=="Demo終了"):
        
        
        # 下をゆっくり不透明化
        if (panel2.get()<127):
            panel2.set(panel2.get()+1)
            time.sleep(0.2)
        # 上をゆっくり不透明化
        elif (panel1.get()<127):
            panel1.set(panel1.get()+1)
            time.sleep(0.2)
        else:
            while(button["text"]=="Demo終了"):
                pass
    panel1.set(0)
    panel2.set(0)
    
    return
        

# 最初に必ず別スレッドに投げてから処理を開始する関数(この関数が別スレッドでdemo_runnningを起動する)
def demo_start(button,panel1,panel2):
    Th_TwoTh = threading.Thread(target = lambda:demo_runnnig(button,panel1,panel2))
    Th_TwoTh.start()




def click_record(button):
    if button["text"] == "Record Start":
        #button["text"] = "Recording..."

        sr = 44100        # サンプリングレート
        framesize = 1024  # フレームサイズ
        idx = 0           # マイクのチャンネル
        t = 6             # 計測時間[s]

        filename = api.record(sr, framesize, idx, t)
        print(filename)
        
        #time.sleep(0.1)
        #button["state"] = tk.DISABLED
        #button["state"] = tk.NORMAL
        #button["text"] = "Record Start"
