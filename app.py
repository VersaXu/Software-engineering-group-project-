import base64
import os
import re

from flask import Flask, render_template, request
import json

from process import *

app = Flask(__name__)
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=1500)


# decoding an image from base64 into raw representation
def convert_image(img_data, name):
    img_str = re.search(r'base64,(.*)', str(img_data)).group(1)
    with open(name + '.png', 'wb') as output:
        output.write(base64.b64decode(img_str))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'png'


@app.route('/')
def index():
    return render_template("index.html")


# 上传文件
@app.route('/upload', methods=['POST'])
def upload():
    print('upload file')
    x = request.files['photo']
    if not x or not allowed_file(x.filename):
        return ''
    else:
        x.save(os.path.join(os.path.dirname(__file__), 'static/pic', 'original.png'))
        return 'success'


@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    print("submit file")
    # get the raw data format of the image
    img_data = request.get_data()
    # encode it into a suitable format
    convert_image(img_data, 'area')
    # process the image
    process_image()
    return '1'


@app.route('/getCanvasParameter/', methods=['POST'])
def getCanvasParameter():
    print("send parameter")
    x = imageio.imread('./static/pic/Original.png', pilmode='L')
    x = np.asarray(x)

    parameter = [x.shape[0], x.shape[1]]

    print(json.dumps(parameter))
    return json.dumps(parameter)


if __name__ == '__main__':
    app.run(debug=True)
    app.jinja_env.auto_reload = True
