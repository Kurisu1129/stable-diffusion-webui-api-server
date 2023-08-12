from flask import Flask
from flask import request
from flask_cors import CORS
import router
import time

app = Flask(__name__)
CORS(app)
@app.route('/sam/sam-predict')
def sam_dino_predict():
    # threshold = request.args.to_dict().get('threshold')
    threshold = request.form.get('threshold')
    return router.sam_init_with_dino(threshold)

@app.route('/inpaint', methods=['POST'])
def inpaint():
    threshold = request.form.get('threshold')
    prompt = request.form.get('prompt')
    return router.inpaint(threshold, prompt)

@app.route('/upload', methods=['POST'])
def save_file():
    file = request.files['file']
    print(request.files.to_dict)
    file.save('../web/src/assets/image/upload/upload.png')
    return 'File saved successfully.'