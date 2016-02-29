from flask import Flask, Blueprint, render_template

app = Flask(__name__)
app.config.from_object("config")

index = Blueprint('index', __name__, template_folder='templates')
app.register_blueprint(index)

api_key = "AIzaSyDAEWcpvx6no3lvWU26WiY4KmH3ZKGLXTc"

@app.route('/')
def hello():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()