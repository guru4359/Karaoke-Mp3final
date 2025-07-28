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
    return render_template('index.html')

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
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
    file.save(filepath)
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
