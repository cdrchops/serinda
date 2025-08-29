from flask import Flask, render_template, send_file
import os
from typing import Dict

app = Flask(__name__)

class PDFReader:
    def __init__(self, root_dir: str):
        """Initialize the PDFReader with the root directory to scan."""
        # Use provided root_dir rather than a hard-coded path
        self.root_dir = "c:/projects/guides/" # root_dir
        self.pdf_files: Dict[str, str] = {}  # rel_path: full_path
        self.index_files()

    def index_files(self) -> None:
        """Index all PDF files in the root directory and its subdirectories."""
        self.pdf_files.clear()
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.root_dir)
                    self.pdf_files[rel_path] = full_path

    def get_directory_structure(self) -> Dict:
        """Return a nested dictionary representing the directory structure."""
        structure = {}
        for rel_path in self.pdf_files.keys():
            parts = rel_path.split(os.sep)
            current = structure
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {'type': 'folder', 'children': {}}
                current = current[part]['children']
            current[parts[-1]] = {'type': 'file', 'path': rel_path}  # Store rel_path
        return structure

# Initialize PDFReader using env var or repo-relative default
def _default_pdf_root() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    content_dir = os.path.join(base_dir, 'content')
    # Prefer a 'content' subdirectory if it exists; otherwise use the pdfViewer directory itself
    return content_dir if os.path.isdir(content_dir) else base_dir

PDF_ROOT = os.environ.get('PDF_ROOT') or _default_pdf_root()
reader = PDFReader(PDF_ROOT)

@app.route('/')
def index():
    """Render the main page with directory structure.
    Re-index on each request so newly added/removed PDFs are reflected.
    """
    reader.index_files()
    structure = reader.get_directory_structure()
    return render_template('index.html', structure=structure)

@app.route('/pdf/<path:rel_path>')
def serve_pdf(rel_path):
    """Serve the PDF file securely."""
    # Prevent path traversal by normalizing and ensuring it's within root
    requested = os.path.normpath(os.path.join(reader.root_dir, rel_path))
    if not requested.startswith(os.path.abspath(reader.root_dir)):
        return "Invalid path", 400
    if not os.path.isfile(requested):
        return "File not found", 404
    return send_file(requested, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)