from app import app
from flask import redirect, url_for, request, render_template, flash, request, make_response, request, send_file
import os
from Bio import Entrez
from Pipeline import Facade
from werkzeug.utils import secure_filename

## Set the allowed file extensions here
ALLOWED = set(['txt', 'fna', 'fasta'])

## Function that determines if a file has a specified file extension. 
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED


## Defines the route that the flask app will go when the user does not specify anything after the first slash. This page has two request forms. A user can navigate to either the NCBI or USER UPLOAD PAGE
## The home HTML template in the templates folder is rendered here.
@app.route('/',methods= ['POST', 'GET'])
def index():
	if request.method == 'POST':
		if "ncbi" in request.form:
			return redirect(url_for('ncbi'))
		if "upload" in request.form:
			return redirect(url_for('upload'))
	else:
		return render_template('home.html')

## Defines the route to the NCBI webpage. The ncbi HTML template in the templates folder will be rendered here.
@app.route('/ncbi', methods= ['POST', 'GET'])
def ncbi():
	return render_template('ncbi.html')

## Defines a method that will be run in the NCBI HTML webpage. 
## If a user enters an invalid RefSeq Accession number(as determined by Biopythons Entrez module), the web page will be refreshed displaying a message that the RefSeq Accession is invalid. 
## The application will call the facade's ncbi method if the RefSeq Accession is valid. The method will take the user input as the argument. The system will change the current working directory to the 
## temporary folder after the pipeline runs. The application will zip up the file into a file named what the user specified. 
## For example the zip file name will be APNU000.zip if the user entered APNU000 in the input. 
## This zip will contain the csv file with the bias statistics and the fasta file containing the highly expressed genes. 
## The file is sent to the user as a download with the send_file function. 
@app.route('/ncbidata', methods = ['POST'])
def my_form_post():
	if request.method == 'POST':
		text = request.form['text']
		facade = Facade()
		try:
			Entrez.email = "bdehlinger@luc.edu"	
			handle = Entrez.efetch(db="nucleotide", id=text)
		except:
			flash('The RefSeq Accession number is invalid')
			return redirect('/ncbi')
		try:
			facade.ncbi(text)
			os.chdir(app.config['UPLOAD_FOLDER'] + "/temp")
			os.system("zip " + str(text) + ".zip " + facade.file + " temporary.fasta")
			os.chdir("..")
			return send_file(app.config['UPLOAD_FOLDER'] + "/temp/" + text +  ".zip", as_attachment=True)
		except:
			flash('There was an error, please make sure the RefSeq Accession has an assembly, and is a bacterial genome. Also please try reuploading the genome. The server may be busy.')
			return redirect('/ncbi')

##This route specifies that the upload HTML file in templates will be rendered in the /upload route.
@app.route('/upload', methods=['POST', 'GET'])
def upload():
	return render_template('upload.html')

## This route specifies the function that will run when the user submits a genome to the web server on the /upload route.
## Seveal errors are handled. User uploaded files are renamed as a secure filename. The facade is created and the uploaded_genome method is called, with theSecureName and the actualName as two different arguments. 
## A zip file is created containing the highly expressed genes and the bias calculations. The user is given the zip file with the send_file argument.
@app.route('/uploader', methods = ['POST'])
def uploader():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash("File not found!")
			return redirect('/upload')
		file = request.files['file']
		if file.filename == '':
			flash('Please select a file to upload')
			return redirect('/upload')
		if file and allowed_file(file.filename):
			try:
				theSecureName = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], theSecureName))
				facade = Facade()
				facade.uploaded_genome(theSecureName, file.filename)
				os.chdir(app.config['UPLOAD_FOLDER'] + "/temp")
				os.system("zip " + str(file.filename) + ".zip " + facade.file + " temporary.fasta")
				os.chdir("..")
				return send_file(app.config['UPLOAD_FOLDER'] + "/temp/" + file.filename +  ".zip", as_attachment=True)
			except:
				flash("There was an error! Please make sure file is in nucleotide fasta format and is a complete genome. Then try reuploading the genome, server may be busy.")
				return redirect('/upload')




