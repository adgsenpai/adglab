from flask import Flask, render_template, request, redirect

app = Flask(__name__,static_folder='assets',template_folder='pages')

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/apps')
def apps():
    return 'oh no im still on construction'

@app.route('/vm')
def vm():
    return 'oh no im still on construction'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000)