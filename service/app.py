from flask import Flask
from flask import request
import router

app = Flask(__name__)

@app.route('/sam/sam-predict')
def sam_dino_predict():
    threshold = request.args.to_dict().get('threshold')
    return router.sam_init_with_dino(threshold)

@app.route('/inpaint')
def inpaint():
    threshold = request.args.to_dict().get('threshold')
    prompt = request.args.to_dict().get('prompt')
    return router.inpaint(threshold, prompt)