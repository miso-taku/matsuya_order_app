import random
from flask import Flask, render_template, jsonify, request
import subprocess
import os
import datetime

from chatgpt_text_gen import ChatGPT

app = Flask(__name__)

unix_time = round(datetime.datetime.now().timestamp())
file_name = f"history/recognized_{unix_time}"

def get_text(fn):
    texts = ""
    if os.path.exists(f"history/{fn}"):
        with open(f"history/{fn}", 'r') as fp:
            texts = "".join([i for i in fp])
    else:
        texts = '申し訳ありません。上手く聞き取れませんでした。'
    return texts

def start_process(unix_time):
    global p
    cmd = f"python whisper_mic/cli.py --time {unix_time}"
    p = subprocess.Popen(cmd.split())
    return p

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_recog():
    print("start")
    if not os.path.exists("history"):
        os.mkdir("history")
    unix_time =  round(datetime.datetime.now().timestamp())
    fn = f"recognized_{unix_time}"
    p = start_process(unix_time)
    print(fn)
    return jsonify({'item':fn})

@app.route('/stop', methods=['POST'])
def stop():
    print("stop")
    global p
    item = ""
    try:
        if p:
            p.kill()
    except:
        item = "failed to stop the process"

    fn = request.json['rfn']
    print(fn)
    item = get_text(fn)
    print(item)
    return jsonify({'item':item})

if __name__ == '__main__':
    app.run(debug=True)
