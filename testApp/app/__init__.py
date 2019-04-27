from flask import Flask


## This is a configuration file. UPLOAD_FOLDER specifies where user uploads will go. 
## The secret_key is necessary to run and should be hard to guess. 
## the MAX_CONTENT_LENGTH can be changed to change how large uploads can be. For example 18 * 1024 * 1024 will allow 18MB uploads. 
UPLOAD_FOLDER = r"/home/bdehlinger/DCB-Dynamic-Codon-Bias/testApp/"
app = Flask(__name__)
app.secret_key = "dragon"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



from app import routes
