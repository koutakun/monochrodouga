import streamlit as st
from time import sleep
from PIL import Image
import numpy as np
import cv2
from math import ceil
import os


st.title("モノクロ動画📺")
st.write("このアプリは動画を白黒に変換し0,1で表すアプリです。")
st.write("動画をアップロードするかDemoに切り替えてStartボタンを押してください")

#初期化
if "count" not in st.session_state:
    st.session_state.count = 1

uploaded_file = st.file_uploader("動画をアップロードしてください") #動画ファイルのアップロード
start = st.button("Start")
stop = st.button("Stop")
rerun = st.button("Rerun")
toggle_demo = st.toggle("Demo")

#デモかどうかで流す動画を切り替える
if toggle_demo:
    dir = "demo"
    file = "badapple.mp4"
else:
    if uploaded_file is not None:
        dir = "images"
        file = "uploaded_file.mp4"
        with open("uploaded_file.mp4","wb") as fw:
            fw.write(uploaded_file.read())
    else:
        st.write("No Video")
        st.stop()


#動画からコマ送り画像を生成
def make_image(file,dir):
    for f in os.listdir(dir):
        os.remove(f"{dir}/{f}")
    cap = cv2.VideoCapture(file)
    fps = ceil(cap.get(cv2.CAP_PROP_FPS))
    cnt = 0
    while True:
        ret, frame = cap.read()
        cnt += 1
        if not ret:
            break
        frame = cv2.resize(frame,dsize=(80,20))
        g_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.imwrite(f"{dir}/{cnt:04}.jpg",g_frame)

if start: #スタート
    make_image(file,dir)
    st.rerun()
if stop: #ストップ
    st.stop()
if rerun: #再起動
    st.session_state.count = 1
    make_image(file,dir)
    st.rerun()

#画像ファイル名を取得
files = os.listdir(dir)
files.sort()

#動画がアップロードされていないとき
if len(files) == 0:
    st.write("No Data")
    st.stop()

#全てのコマを流したとき
if st.session_state.count >= len(files):
    st.write("END")
    st.stop()

#画像を表示
img = np.array(Image.open(f"{dir}/{files[st.session_state.count]}").convert("L"))
st.write("".join(["".join(map(str,(i<128)*1)) + "\n" for i in img]))

#次のコマに移行
st.session_state.count += 1
sleep(0.025)
st.rerun()