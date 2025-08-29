import os
import re
from typing import List, Dict


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

    def search_files(self, query: str, case_sensitive: bool = False) -> List[Dict[str, str]]:
        """Search for a query string in all indexed markdown files."""
        results = []
        for file_path, content in self.markdown_files.items():
            # Prepare content and query based on case sensitivity
            search_content = content if case_sensitive else content.lower()
            search_query = query if case_sensitive else query.lower()

            # Find all matches with line numbers
            matches = []
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                search_line = line if case_sensitive else line.lower()
                if search_query in search_line:
                    matches.append({
                        'line_number': line_num,
                        'line_content': line.strip()
                    })

            if matches:
                results.append({
                    'file_path': file_path,
                    'matches': matches
                })

        return results

    def get_file_content(self, file_path: str) -> str:
        """Retrieve the full content of a specific markdown file."""
        return self.markdown_files.get(file_path, "File not found or not indexed.")


def main():
    # Example usage
    directory = input("Enter the directory to scan for markdown files: ")
    reader = MarkdownReader(directory)

    print(f"Found {len(reader.markdown_files)} markdown files.")

    while True:
        query = input("Enter search query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        results = reader.search_files(query)

        if not results:
            print("No matches found.")
            continue

        for result in results:
            print(f"\nFile: {result['file_path']}")
            for match in result['matches']:
                print(f"Line {match['line_number']}: {match['line_content']}")

        # Optionally, view full content of a specific file
        view_file = input("\nEnter file path to view full content (or press Enter to skip): ")
        if view_file:
            content = reader.get_file_content(view_file)
            print(f"\nContent of {view_file}:\n{content}")


if __name__ == "__main__":
    main()