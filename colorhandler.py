"""
colorhandler.py
A flask script that handles requests to change GPIO PWN through the pi-blaster library
Stephen Greene
"""
from __future__ import print_function
from flask import Flask, redirect, request, render_template
from pathlib import Path
import time
app = Flask(__name__)


@app.route('/set', methods=['GET', 'POST'])
def colorhandler():
    f = open(str(Path("/dev/pi-blaster").absolute()), "w", 0)       # "w" forces file flush every print
    color = request.form['color']
    timer = int(request.form['timer'])
    loop = int(request.form['loop'])
    red = "22=" + "%.3f" % (int(color[:2], 16) / 255.0)
    green = "23=" + "%.3f" % (int(color[2:4], 16) / 255.0)
    blue = "24=" + "%.3f" % (int(color[4:], 16) / 255.0)
    print(red, file=f)
    print(green, file=f)
    print(blue, file=f)

    if timer != 0 and loop > 0:
        for x in range(0, loop):
            time.sleep(timer / 100.0)
            print("22=0", file=f)
            print("23=0", file=f)
            print("24=0", file=f)
            time.sleep(timer / 100.0)
            print(red, file=f)
            print(green, file=f)
            print(blue, file=f)
            x += 1

    return "Color: " + request.form[color] + "Timer: " + request.form['timer'] + "Loop: " + request.form['loop']


@app.route('/')
def index():
    return "use /set with color, timer, and loop args"

if __name__ == '__main__':
   app.run()

