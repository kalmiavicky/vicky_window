from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html.jinja')

@app.route('/new')
def new():
    return "<h1>最新課表</h1>"
    # return render_template('index.html.jinja')

@app.route('/youbike')
def youbike():
    return render_template('index.html.jinja')

@app.route('/contact')
def contact():
    # show the post with the given id, the id is an integer
    return render_template('index.html.jinja')