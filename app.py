from flask import Flask, escape, render_template, request, redirect,url_for, jsonify, send_file, session, flash
import logging
from logging.handlers import RotatingFileHandler 


app = Flask(__name__)
app.secret_key = 'my_secret_key'

app.logger.name='myapp'

handler = RotatingFileHandler('myapp.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


@app.route('/jsondata')
def jsondata():
    data = {'name':'Dhruvik', 'age':30}
    return jsonify(data)

@app.route("/download")
def download():
    file_name='example.txt'
    return send_file(file_name, as_attachment=True)



@app.route("/home")
def home():
    app.logger.info('Home page is loaded')
    return render_template("home.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username=='admin' and password == 'admin':
        flash('Login successful')
        app.logger.info("logged in successfully")
        session['logged_in_user'] = username
        return redirect(url_for("dashboard"))
    else:
        app.logger.warn('Invalid credentials')
        return render_template("home.html", error="True")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    # requests = request.args.to_dict()
    # username = requests['username']

    if 'logged_in_user' in session:
        username = session['logged_in_user']
    else :
        return redirect(url_for('home'))
    
    return render_template("dashboard.html", username=username)

@app.route("/logout")
def logout():
    flash('You have been logged out successfully!')
    session.pop('logged_in_user', None)
    return redirect(url_for('home'))

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(400)
def internal_error1(error):
    return render_template('500.html'), 500

@app.route("/")
def hello_world():
    name = 'Alex'

    kwargs = {
        "name": name,
        "template_name":"Jinja2"
    }
    return render_template("jinja_intro.html", **kwargs)

@app.route("/conditional")
def conditional_stmt():
    kwargs = {
        "company": "Simplilearn"
    }
    return render_template("conditional.html", **kwargs)

@app.route("/looping")
def looping():

    planets = {
        "Mercury",
        "Venus",
        "Earth",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune"
    }
    kwargs = {
        "planets": planets
    }
    return render_template("loopings.html", **kwargs)



@app.route("/first")
def greetings():
    return render_template("first.html")

@app.route("/second")
def greetings_second():
    return render_template("second.html")


# Flask allows you to interpolate string in the template