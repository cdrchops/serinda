from flask import Flask, render_template, request, send_file
import jinja2

app = Flask(__name__)

my_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader('./')])
app.jinja_loader = my_loader

@app.route("/")
def index(pth=""):
    text = request.args.get('pth', "", type=str)
#     with open("/mnt/c/projects/obsidianSync/reports/27Apr24.md", "r") as f:
    pth = 'c:/projects/obsidianSync/{}'.format(text)
    with open(pth, "r", encoding="utf8") as f:
        contents = f.read()

    return render_template("index.html", contents=contents)

if __name__ == "__main__":
    app.run(debug=True)

# http://localhost:5000/?pth=reports/28Apr24.md
# http://localhost:5000/?pth=notes/007-Serinda/Architecture.md