from flask import Flask, render_template, redirect, request, jsonify
from flaskext.mysql import MySQL
import bcrypt, os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['DB_PASS']
app.config['MYSQL_DATABASE_DB'] = 'nevermore'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    cursor.execute("SELECT * FROM users WHERE username = %s", request.form['username'])
    result = cursor.fetchone()
    token = bcrypt.gensalt()

    if result is None:
        password = request.form['password'].encode('utf-8')
        hash = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor.execute("INSERT INTO users VALUES (DEFAULT, %s, %s, %s, %s, %s)",
                       (request.form['username'], hash, request.form['email'], request.form['name'], token))
        conn.commit()
    else:
        return jsonify(status=401)

    return jsonify(status=200, token=token)


@app.route('/login', methods=['POST'])
def login():
    req_pass = request.form['password'].encode('utf-8')
    cursor.execute("SELECT password FROM users WHERE username = %s", (request.form['username']))

    result = cursor.fetchone()

    if result is None:
        return jsonify(status=401)

    if bcrypt.checkpw(req_pass, result[0].encode('utf-8')):
        token = bcrypt.gensalt()

        cursor.execute("UPDATE users SET token = %s WHERE username = %s", (token, request.form['username']))
        conn.commit()
        return jsonify(status=200, token=token)
    else:
        return jsonify(status=401)


@app.route('/auth', methods=['POST'])
def auth():
    req_token = request.form['token']
    cursor.execute("SELECT token FROM users WHERE token = %s", req_token)

    if cursor.fetchone() is not None:
        return jsonify(status=200)
    else:
        return jsonify(status=401)


@app.route('/get_user', methods=['POST'])
def get_username():
    req_token = request.form['token']
    cursor.execute("SELECT username, email, full_name FROM users WHERE token = %s", req_token)

    result = cursor.fetchone()

    if result is not None:
        return jsonify(status=200, username=result[0], email=result[1], name=result[2])
    else:
        return jsonify(status=401)


@app.route('/quoth', methods=['POST'])
def quoth():
    pass


@app.route('/requoth', methods=['POST'])
def requoth():
    pass


if __name__ == '__main__':
    app.run(debug=True)
