import os
import tempfile
import zipfile
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils.converters import convert_file_dispatch

ALLOWED_EXTENSIONS = set(['pdf','xls','xlsx','jpg','jpeg','png','ppt','pptx'])

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'supersecret')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    # support multiple files
    files = request.files.getlist('files')
    tool = request.form.get('tool')  # e.g., pdf_to_excel, excel_to_pdf, jpg_to_excel ...

    if not files or len(files) == 0:
        flash('No files uploaded')
        return redirect(url_for('index'))

    tmpdir = tempfile.mkdtemp()
    outputs = []

    try:
        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                in_path = os.path.join(tmpdir, filename)
                f.save(in_path)

                out_path = convert_file_dispatch(in_path, tool, tmpdir)
                if out_path:
                    outputs.append(out_path)

        if not outputs:
            flash('Conversion produced no outputs')
            return redirect(url_for('index'))

        # If single file uploaded and single output, return file directly
        if len(outputs) == 1:
            return send_file(outputs[0], as_attachment=True)

        # Otherwise bundle to zip
        zip_path = os.path.join(tmpdir, 'results.zip')
        with zipfile.ZipFile(zip_path, 'w') as z:
            for p in outputs:
                z.write(p, arcname=os.path.basename(p))
        return send_file(zip_path, as_attachment=True, download_name='results.zip')

    finally:
        # Note: temp dir not removed immediately for debugging; could remove in production
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
