from flask import Flask, send_from_directory, request
from flask_cors import CORS
import router
import time

app = Flask(__name__)
CORS(app)
@app.route('/sam/sam-predict')
def sam_dino_predict():
    # threshold = request.args.to_dict().get('threshold')
    threshold = request.form.get('threshold')
    dinoprompt = request.form.get('dinoprompt')
    return router.sam_init_with_dino(threshold, dinoprompt)

@app.route('/inpaint', methods=['POST'])
def inpaint():
    threshold = request.form.get('threshold')
    prompt = request.form.get('prompt')
    dinoprompt = request.form.get('dinoprompt')
    return router.inpaint(threshold, prompt, dinoprompt)

@app.route('/upload', methods=['POST'])
def save_file():
    file = request.files['file']
    print(request.files.to_dict)
    file.save('../web/src/assets/image/upload/upload.png')
    return 'File saved successfully.'

@app.route('/image/<path:filename>')
def get_image(filename):
    image_folder = './image/output/'  # Replace with the actual path to your image folder
    return send_from_directory(image_folder, filename)
