from app import app
from flask import redirect, url_for, request, render_template, flash, request, make_response, request, send_file
import os
from Bio import Entrez
from Pipeline import Facade
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import io
import tempfile
import requests



import logging
import traceback

logger = logging.getLogger("DCB")
handle = logging.FileHandler('/var/log/tmp/DCB.log', 'w')
logger.addHandler(handle)
logger.setLevel("DEBUG")


## Set the allowed file extensions here
ALLOWED = set(['txt', 'fna', 'fasta'])

## Function that determines if a file has a specified file extension. 
def _allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

# Command to execute an in memory zip
def _execute_zip_files(*args):
	data = io.BytesIO()
	with ZipFile(data, mode='w') as zip_of_files:
		for file_to_zip in args:
			zip_of_files.write(file_to_zip)
	data.seek(0)
	return data


## Command to send a file
def _execute_send_file(data, name_of_zip_file):
	return send_file(data, attachment_filename = name_of_zip_file, as_attachment=True)
	






## Defines the route that the flask app will go when the user does not specify anything after the first slash. This page has two request forms. A user can navigate to either the NCBI or USER UPLOAD PAGE
## The home HTML template in the templates folder is rendered here.
@app.route('/',methods= ['POST', 'GET'])
@app.route('/index', methods = ['POST', 'GET'])
def index():
	if request.method == 'POST':
		if "ncbi" in request.form:
			return redirect(url_for('ncbi', external=True))
		if "upload" in request.form:
			return redirect(url_for('upload', external=True))
		if "ncbiassembly" in request.form:
			return redirect(url_for('ncbiassembly', external=True))
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
## The zip file is buffered in memory. The file is served to the user and the temporary folder is deleted! We utilize only temporary folders throughout this whole process and use context managers to garbage collect after these folders and files are no longer needed to avoid clutter on the server.
@app.route('/ncbidata', methods = ['POST'])
def my_form_post():
	if request.method == 'POST':
		text = request.form['text']
		facade = Facade()
		try:
			os.chdir(app.config['UPLOAD_FOLDER'])
			with tempfile.TemporaryDirectory(dir=os.getcwd()) as tempdir:
				temp = tempdir.rsplit('/', 1)[-1]
				os.chdir(tempdir)
				facade.ncbi(text, temp)
				if os.path.isfile(text + "errors.txt"):
					zip_of_files = _execute_zip_files(facade.file, "HEGS.fasta", text + "errors.txt")
				else: 
					zip_of_files = _execute_zip_files(facade.file, "HEGS.fasta")
				os.chdir("..")
				return _execute_send_file(zip_of_files, text + ".zip")
		except Exception as e:
			logger.exception("Exception has occured in routes.py at my_form_post method")
			flash('Please make sure the RefSeq Accession has an assembly, and is a bacterial genome. Also please try reuploading the genome. The server may be busy.')
			return redirect('/ncbi')
	

##This route specifies that the upload HTML file in templates will be rendered in the /upload route.
@app.route('/upload', methods=['POST', 'GET'])
def upload():
	return render_template('upload.html')

## This route specifies the function that will run when the user submits a genome to the web server on the /upload route.
## Seveal errors are handled. User uploaded files are renamed as a secure filename. The facade is created and the uploaded_genome method is called, with theSecureName and the actualName as two different arguments. 
## A zip file is created containing the highly expressed genes and the bias calculations. The user is given the zip file with the send_file argument.
## The zip file is buffered into memory. This file is served to the user and the temporary folder is deleted. We utilize only temporary folders throughout this whole process and use context managers to garbage collect after these folders and files are no longer needed to avoid clutter on the server.
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
		if file and _allowed_file(file.filename):
			try:
				theSecureName = secure_filename(file.filename)
				if (theSecureName == ''):
					theSecureName = "YourGenome"	
				facade = Facade()
				os.chdir(app.config['UPLOAD_FOLDER'])
				with tempfile.TemporaryDirectory(dir=os.getcwd()) as tempdir:
					temp = tempdir.rsplit('/', 1)[-1]
					file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/' + temp, theSecureName))
					os.chdir(tempdir)
					facade.uploaded_genome(theSecureName, temp)
					if os.path.isfile(theSecureName + "errors.txt"):
						zip_of_files = _execute_zip_files(facade.file, "HEGS.fasta", theSecureName + "errors.txt")
					else: 
						zip_of_files = _execute_zip_files(facade.file, "HEGS.fasta")
					os.chdir("..")
					return _execute_send_file(zip_of_files, theSecureName + ".zip")
			except Exception as e:
				logger.exception("Exception has occured in routes.py at uploader method")
				flash("There was an error! Please make sure file is in nucleotide fasta format and is a complete genome. Then try reuploading the genome, server may be busy.")
				return redirect('/upload')
		else: 
			flash("Only upload a .fasta, .fna, or .txt file")
			return redirect('/upload')


@app.route('/ncbiassembly', methods= ['POST', 'GET'])
def ncbiassembly():
	return render_template('ncbiassembly.html')


@app.route('/ncbiassemblydata', methods = ['POST'])
def assembly_post():
	if request.method == 'POST':
		text = request.form['text']
		facade = Facade()
		try:
			the_request = requests.get("https://ncbi.nlm.nih.gov/assembly/" + text)
			if the_request.status_code == 404:
			    raise ValueError("The RefSeq Assemmbly Accession number is invalid")
		except ValueError as e:
			loggger.exception("Exception has occured in routes.py at assembly_post method")
			flash('The RefSeq Assembly Accession number is invalid')
			return redirect('/ncbiassembly')
			
		try:
			os.chdir(app.config['UPLOAD_FOLDER'])
			with tempfile.TemporaryDirectory(dir=os.getcwd()) as tempdir:
				temp = tempdir.rsplit('/', 1)[-1]
				os.chdir(tempdir)
				facade.ncbiassembly(text, temp)
				if os.path.isfile(text + "errors.txt"):
					zip_of_files = _execute_zip_files(facade.file, "HEGS.fasta", text + "errors.txt")
				else: 
					zip_of_files = _execute_zip_files(facade.file, "HEGS.fasta")
				os.chdir("..")
				return _execute_send_file(zip_of_files, text + ".zip")
		except Exception as e:
			logger.exception("Exception has occured in routes.py at assembly_post method")
			flash('There was an error, please make sure the RefSeq Accession has an assembly, and is a bacterial genome. Also please try reuploading the genome. The server may be busy.')
			return redirect('/ncbiassembly')

	
	


