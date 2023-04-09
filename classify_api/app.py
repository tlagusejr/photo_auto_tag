import predict
import sys
import requests
from io import BytesIO
from flask import Flask, request, jsonify
import base64
import PIL
app = Flask(__name__)

@app.route('/api',methods=['POST'])
def prediction():
    data = request.get_json(force=True)
    im_b64 = data["image"]
    image = base64.b64decode(im_b64)
    image = BytesIO(image)
    output = predict.predict(image)
    
    
    return jsonify(output)
@app.route("/hello",methods=['get'])
def hello():
    
    return "Hello"

if __name__ == '__main__':
    host_port = "0.0.0.0"
    try:
        app.run(host = host_port, port=int(sys.argv[1]), debug=False)
    except:
        app.run(host = host_port, port=8123,debug=False)
