from flask import Flask

UPLOAD_FOLDER = r"/home/bdehlinger/DCB-Dynamic-Codon-Bias/testApp/"
app = Flask(__name__)
app.secret_key = "dragon"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



from app import routes
