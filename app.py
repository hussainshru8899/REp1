import os
import sys
import tempfile
import zipfile
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Add project root to Python path to ensure utils is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.converters import convert_file_dispatch  # Your custom converter module

# Allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'xls', 'xlsx', 'jpg', 'jpeg', 'png', 'ppt', 'pptx'}

# Flask setup
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'supersecret')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render home page."""
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """Handle file conversion."""
    files = request.files.getlist('files')
    tool = request.form.get('tool')  # e.g., pdf_to_excel, excel_to_pdf, jpg_to_excel ...

    if not files:
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

        # If only one output, return directly
        if len(outputs) == 1:
            return send_file(outputs[0], as_attachment=True)

        # Otherwise bundle all outputs into a zip
        zip_path = os.path.join(tmpdir, 'results.zip')
        with zipfile.ZipFile(zip_path, 'w') as z:
            for p in outputs:
                z.write(p, arcname=os.path.basename(p))
        return send_file(zip_path, as_attachment=True, download_name='results.zip')

    finally:
        # Optional: cleanup temp directory after sending files
        for f in outputs + [zip_path] if len(outputs) > 1 else outputs:
            try:
                os.remove(f)
            except Exception:
                pass
        try:
            os.rmdir(tmpdir)
        except Exception:
            pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
