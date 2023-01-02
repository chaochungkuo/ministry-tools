import os
import os
import glob
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from levtools.core.bible import Bible
from levtools.core.textbody import TextBody
from levtools.core.modifier import Modifier

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'docx', "txt"}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
# app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_verses_en2de(path, filename):
    mod = Modifier("EN")
    inputfile = TextBody(path=path, format="book")
    mod.identify_scriptures(inputfile)
    mod.convert_en2de(inputfile)
    mod.add_de_lines(inputfile)
    mod.print_scriptures(inputfile, with_text=True)
    output_file = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    inputfile.save_docx(output_file, ref=True, de=True)

def add_verses_de2de(path, filename):
    mod = Modifier("DE")
    inputfile = TextBody(path=path, format="book")
    mod.identify_scriptures(inputfile)
    mod.print_scriptures(inputfile, with_text=True)
    output_file = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    inputfile.save_docx(output_file, ref=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    files = glob.glob(app.config['UPLOAD_FOLDER']+'/*')
    for f in files:
        os.remove(f)
    files = glob.glob(app.config['DOWNLOAD_FOLDER']+'/*')
    for f in files:
        os.remove(f)
    return render_template('index.html')


@app.route('/verse_de2de', methods=['GET', 'POST'])
def verse_de2de():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            add_verses_de2de(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('verse_de2de.html')

@app.route('/verse_en2de', methods=['GET', 'POST'])
def verse_en2de():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            add_verses_en2de(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('verse_en2de.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
