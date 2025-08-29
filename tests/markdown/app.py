from flask import Flask, render_template, request, jsonify
import os
import markdown
from typing import List, Dict

app = Flask(__name__)

class MarkdownReader:
    def __init__(self, root_dir: str):
        """Initialize the MarkdownReader with the root directory to scan."""
        self.root_dir = root_dir
        self.markdown_files: Dict[str, str] = {}
        self.index_files()

    def index_files(self) -> None:
        """Index all markdown files in the root directory and its subdirectories."""
        self.markdown_files.clear()
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            self.markdown_files[file_path] = content
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    def get_directory_structure(self) -> Dict:
        """Return a nested dictionary representing the directory structure."""
        structure = {}
        for file_path in self.markdown_files.keys():
            # Get relative path from root_dir
            rel_path = os.path.relpath(file_path, self.root_dir)
            parts = rel_path.split(os.sep)
            current = structure
            # Build folder structure
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {'type': 'folder', 'children': {}}
                current = current[part]['children']
            # Add file
            current[parts[-1]] = {'type': 'file', 'path': file_path}
        return structure

    def get_file_content(self, file_path: str) -> str:
        """Retrieve the full content of a specific markdown file."""
        return self.markdown_files.get(file_path, "File not found or not indexed.")

    def save_file_content(self, file_path: str, content: str) -> bool:
        """Save content to a markdown file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.index_files()  # Re-index after saving
            return True
        except Exception as e:
            print(f"Error saving {file_path}: {e}")
            return False

# Initialize MarkdownReader (set your directory path here)
reader = MarkdownReader('e:/obsidianSync/notes/')

@app.route('/')
def index():
    """Render the main page with directory structure."""
    structure = reader.get_directory_structure()
    return render_template('index.html', structure=structure)

@app.route('/file/<path:file_path>')
def get_file(file_path):
    """Get the content of a specific file, including rendered HTML."""
    content = reader.get_file_content(file_path)
    if content == "File not found or not indexed.":
        return jsonify({'content': content, 'html': content})
    # Convert markdown to HTML
    html_content = markdown.markdown(content, extensions=['extra', 'codehilite'])
    return jsonify({'content': content, 'html': html_content})

@app.route('/save/<path:file_path>', methods=['POST'])
def save_file(file_path):
    """Save the edited content of a file."""
    content = request.json.get('content')
    success = reader.save_file_content(file_path, content)
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(debug=True)
