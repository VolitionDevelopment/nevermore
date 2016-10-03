from flask import Flask
from flaskext.mysql import MySQL
import bcrypt

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
