from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', output_url=None)

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_file' not in request.files:
        flash("No file uploaded.")
        return redirect(url_for('index'))

    file = request.files['audio_file']
    if file.filename == '':
        flash("No selected file.")
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4()}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    file.save(filepath)
    return render_template('index.html', output_url=url_for('download_file', filename=unique_name))

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)
