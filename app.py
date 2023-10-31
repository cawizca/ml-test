from flask import Flask
import warnings
warnings.filterwarnings("ignore")

from fertilizerPredict import fertilizerPrediction
from burnDamage import damage_classify

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return '<h1>Hello, World!</h1>'

@app.route("/test", methods=['GET'])
def testing():
    return 'testing'

@app.route("/fertilizer-predict", methods=['POST'])
def prediction():
    output = fertilizerPrediction()
    return output

@app.route("/damage_classify", methods=['POST'])
def burnDamage():
    output = damage_classify()
    return output

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
