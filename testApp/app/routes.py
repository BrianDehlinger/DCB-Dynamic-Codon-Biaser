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
			os.chdir(app.config['UPLOAD_FOLDER'] + "/temp")
			os.system("zip " + str(text) + ".zip " + facade.file + " temporary.fasta")
			os.chdir("..")
			return send_file(app.config['UPLOAD_FOLDER'] + "/temp/" + text +  ".zip", as_attachment=True)
		except:
			flash('There was an error, please make sure the RefSeq Accession has an assembly, and is a bacterial genome. Also please try reuploading the genome. The server may be busy.')
			return redirect('/ncbi')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
	return render_template('upload.html')


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




