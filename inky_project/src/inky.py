import urllib.request
import os,random,time,signal
from flask import Flask, flash, request, redirect, url_for,render_template
from inky.auto import auto
from PIL import ImageDraw,Image 

print("Inky.py is running")

@app.route('/', methods=['GET', 'POST'])
def root_request():
    print('Received new request!')

    if request.method == 'POST':
        print('Got POST request!')
        print(request.method)
        print(request.form)
        print(request.form.getlist("text")[0])
    return render_template('main.html')

if __name__ == '__main__':
    app.secret_key = str(random.randint(100000,999999))
    app.run(host="0.0.0.0",port=80)