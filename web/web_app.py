from flask import Flask, render_template

app = Flask(__name__, template_folder='/web')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets/<string:page_name>')
def render_static(page_name):
    return render_template('static/%s' % page_name)
    
if __name__ == '__main__':
    app.run()
