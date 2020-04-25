import os
import flask


app = flask.Flask(__name__, static_url_path = '', static_folder='/web/static', template_folder='web/templates')

@app.route('/')
def index():
    """ renderiza o index.html"""
    
    return flask.render_template('index.html')



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
