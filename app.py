from flask import Flask, render_template
from werkzeug.utils import secure_filename
from flask import request
import os

UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = set(['txt'])

path = os.path
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# check for specific file extension


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# check for pattern occurance


def analyse_pattern(bug, analyse):
    pattern = bug.replace('\n', '').replace(' ', '')
    match_pattern = analyse.replace('\n', '').replace(' ', '')
    return match_pattern.count(pattern)

# welcome page


@app.route('/')
def upload_file():
    return render_template('index.html')

# handle file upload/save/and pattern match/ return results of pattern check


@app.route('/display', methods=['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        file_bug = request.files['file_bug']
        file_analyse = request.files['file_analyse']
        is_file_bug_allowed = file_bug and allowed_file(file_bug.filename)
        is_file_analyse_allowec = file_analyse and allowed_file(
            file_analyse.filename)
        if is_file_bug_allowed and is_file_analyse_allowec:
            filename_bug = secure_filename(file_bug.filename)
            filename_analyse = secure_filename(file_analyse.filename)

            file_bug.save(path.join(app.config['UPLOAD_FOLDER'], filename_bug))
            file_analyse.save(
                path.join(app.config['UPLOAD_FOLDER'], filename_analyse))

            bug = open(app.config['UPLOAD_FOLDER'] + filename_bug, "r").read()
            analyse = open(app.config['UPLOAD_FOLDER'] +
                           filename_analyse, "r").read()

        return render_template('content-count.html', content=analyse_pattern(bug, analyse))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7007)
