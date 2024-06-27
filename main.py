from flask import Flask, request, render_template

app = Flask(__name__)


#create routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


#python main
if __name__ == "__main__":
    app.run(debug=True)
