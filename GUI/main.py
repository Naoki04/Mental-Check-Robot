# -*- coding:utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import time
import socket
from datetime import datetime
from tkinter.font import Font

from events import *



# APIにsendし続ける関数
def demo_runnnig(panel1,panel2):

    return
        

# 最初に必ず別スレッドに投げてから処理を開始する関数(この関数が別スレッドでdemo_runnningを起動する)
def controll_start(panel1,panel2):
    Th_TwoTh = threading.Thread(target = lambda:demo_runnnig(panel1,panel2))
    Th_TwoTh.start()


if __name__=="__main__":
    # アプリの作成
    app = tk.Tk()

    # アプリの画面設定
    ## アプリ画面のサイズ
    app.geometry("600x1200" )
    # アプリのタイトル
    app.title("Demo")

    """"""
    # タイトル
    title = tk.Label(
        app, # ラベルの作成先アプリ
        font = ("System", 20), # ラベルのフォント
        text = "Mental Check Bot" # ラベルに表示するテキスト
    )
    title.place(
        x = 30, # ラベルの配置先座標x
        y = 20, # ラベルの配置先座標y
    )

    # パネル1のラベル
    panel1_label = tk.Label(
        app, # ラベルの作成先アプリ
        font = ("System", 18), # ラベルのフォント
        text = "Message from AI" # ラベルに表示するテキスト
    )
    panel1_label.place(
        x = 40, # ラベルの配置先座標x
        y = 80, # ラベルの配置先座標y
    )

    # text area
    message = tk.Text(
        app, # ラベルの作成先アプリ
        height=15,
        width=50
    )
    message.configure(font=Font(family='system', size=16))
    message.pack()
    message.place(
        x = 40,
        y = 120,
    )
    message.insert("2.0", "message from AI is written hereaaaa ...")

    # Button
    record_button = tk.Button(
        app, # ボタンの作成先アプリ
        text = "Record Start", # ボタンに表示するテキスト
        command = lambda: click_record(record_button), # ボタンクリック時に実行する関数
        disabledforeground="darkgray"
    )
    # ボタンの配置
    record_button.place(
        x = 220, # ボタンの配置先座標x
        y = 420, # ボタンの配置先座標y
    )

    """処理はここに記述 """

    # アプリの待機
    app.mainloop()