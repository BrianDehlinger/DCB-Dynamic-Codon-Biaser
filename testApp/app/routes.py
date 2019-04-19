from app import app
from flask import redirect, url_for, request, render_template, flash, request, make_response, request, send_file
import os
from Bio import Entrez
from Pipeline import Facade
from werkzeug.utils import secure_filename

ALLOWED = set(['txt', 'fna', 'fasta'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED


@app.route('/index',methods= ['POST', 'GET'])
def index():
	if request.method == 'POST':
		if "ncbi" in request.form:
			return redirect(url_for('ncbi'))
		if "upload" in request.form:
			print("here")
			return redirect(url_for('upload'))
	else:
		return render_template('home.html')

@app.route('/ncbi', methods= ['POST', 'GET'])
def ncbi():
	return render_template('ncbi.html')

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
			return send_file(facade.file, as_attachment=True)
		except:
			flash('There was an error, please make sure the RefSeq Accession has an assembly, and is for a complete bacterial genome. Please notify the administrator of any other errors!')
			return redirect('/ncbi')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
	return render_template('upload.html')


@app.route('/uploader', methods = ['POST'])
def uploader():
	if request.method == 'POST':
		if 'file' not in request.files:
			print("ERROR FILE NOT IN REQUEST.FILES")
			return redirect('/upload')
		file = request.files['file']
		if file.filename == '':
			flash('Please select a file to upload')
			return redirect('/upload')
		if file and allowed_file(file.filename):
			filename = "temporaryFile"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('Your file has successfully been uploaded to the server')
			facade = Facade()
			facade.uploaded_genome()
			response = make_reponse(result)
			response.headers["Content-Disposition"] = "attachment; filename=result.csv"
			return response



