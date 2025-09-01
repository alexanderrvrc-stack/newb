from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello, World!</h1><p>My first Python website!</p>'

@app.route('/about')
def about():
    return '<h1>About Me</h1><p>This is my about page!</p>'

if __name__ == '__main__':
    app.run(debug=True)
