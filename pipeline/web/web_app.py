from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def render_static():
    return render_template('index.html')

# @app.route('/<string:page_name>/')
# def render_static(page_name):
#     return render_template('%s.html' % page_name)
    
if __name__ == '__main__':
    app.run()
