from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/create')
def create():
    return render_template('Profile_Create.html')

@app.route('/post')
def post():
    return render_template('Post_Page.html')

@app.route('/feed')
def feed():
    return render_template('Feed_page.html')

if __name__ == "__main__":
    app.run()