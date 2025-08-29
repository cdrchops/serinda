from flask import Flask, render_template, redirect, url_for, request
import os
import markdown
from pathlib import Path
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random secret key

# Base directory path (modify as needed)
BASE_DIR = Path(__file__).parent / "content"

class MarkdownForm(FlaskForm):
    filename = StringField('Filename (without .md)', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')

class EditForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class DirForm(FlaskForm):
    dirname = StringField('Directory Name', validators=[DataRequired()])
    submit = SubmitField('Create')

@app.route('/')
@app.route('/<path:subpath>')
def index(subpath=''):
    # Construct the full path
    current_path = BASE_DIR / subpath
    
    # Ensure the path exists and is within BASE_DIR
    if not current_path.exists() or not str(current_path).startswith(str(BASE_DIR)):
        return "Invalid path", 404

    if current_path.is_file() and current_path.suffix == '.md':
        # Read and convert markdown to HTML
        with open(current_path, 'r', encoding='utf-8') as file:
            content = markdown.markdown(file.read())
        return render_template('markdown.html', content=content, current_path=subpath)

    # Get directory contents
    directories = []
    files = []
    for item in current_path.iterdir():
        if item.is_dir():
            directories.append(item.name)
        elif item.is_file() and item.suffix == '.md':
            files.append(item.name)

    directories.sort()
    files.sort()

    # Calculate parent directory path
    parent_path = os.path.dirname(subpath) if subpath else ''

    return render_template('directory.html', 
                         directories=directories, 
                         files=files, 
                         current_path=subpath,
                         parent_path=parent_path)

@app.route('/create/<path:dirpath>', methods=['GET', 'POST'])
def create_file(dirpath=''):
    current_dir = BASE_DIR / dirpath
    if not current_dir.is_dir():
        return "Invalid directory", 404

    form = MarkdownForm()
    if form.validate_on_submit():
        filename = form.filename.data + '.md'
        file_path = current_dir / filename
        if file_path.exists():
            return "File already exists", 400
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(form.content.data)
        return redirect(url_for('index', subpath=dirpath))

    return render_template('form.html', form=form, action='Create File', dirpath=dirpath)

@app.route('/edit/<path:filepath>', methods=['GET', 'POST'])
def edit_file(filepath):
    file_path = BASE_DIR / filepath
    if not file_path.is_file() or file_path.suffix != '.md':
        return "Invalid file", 404

    dirpath = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    with open(file_path, 'r', encoding='utf-8') as f:
        initial_content = f.read()

    form = EditForm(data={'content': initial_content})
    if form.validate_on_submit():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(form.content.data)
        return redirect(url_for('index', subpath=dirpath))

    return render_template('form.html', form=form, action='Edit File', dirpath=dirpath, filename=filename)

@app.route('/delete/<path:filepath>', methods=['POST'])
def delete_file(filepath):
    file_path = BASE_DIR / filepath
    if not file_path.is_file() or file_path.suffix != '.md':
        return "Invalid file", 404

    form = DeleteForm()
    if form.validate_on_submit():
        os.remove(file_path)
        dirpath = os.path.dirname(filepath)
        return redirect(url_for('index', subpath=dirpath))

    return "Invalid request", 400

# <path:dirpath>
@app.route('/create_dir/', methods=['GET', 'POST'])
def create_dir(dirpath=''):
    current_dir = BASE_DIR / dirpath
    # if not current_dir.is_dir():
    #     return "Invalid directory", 404
    print("this is here")
    form = DirForm()
    if form.validate_on_submit():
        new_dir = current_dir / form.dirname.data
        if new_dir.exists():
            return "Directory already exists", 400
        new_dir.mkdir()
        return redirect(url_for('index', subpath=dirpath))

    return render_template('form.html', form=form, action='Create Directory', dirpath=dirpath)

if __name__ == '__main__':
    app.run(debug=True)