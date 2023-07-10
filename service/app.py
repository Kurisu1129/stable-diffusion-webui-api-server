from flask import Flask
import router

app = Flask(__name__)

@app.route('/sam/dino-predict')
def sam_dino_predict():
    return router.sam_init()

@app.route('/inpaint')
def inpaint():
    return router.