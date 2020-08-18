import os
from datetime import date, timedelta

from flask import (Flask, flash, redirect, render_template, request, send_file,
                   session, url_for)
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.view import ModelView
from flask_sqlalchemy import SQLAlchemy
#from flask_uploads import uploaded_file
from sqlalchemy.types import LargeBinary
from io import BytesIO
#from flask_mail import Mail
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'zip', 'jpg', 'jpeg', 'png', 'gif'}
app = Flask(__name__)
app.secret_key = "jfk12e4423"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jattuesday.db'
app.permanent_session_lifetime = timedelta(minutes=10)
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['MAX_CONTENT_PATH'] = '650000'
db = SQLAlchemy(app)
admin = Admin(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(100), unique=True, nullable=False)
    profile_passwd = db.Column(db.String(100), nullable=False)
    profile_email = db.Column(db.String(100), nullable=False)
    profile_number = db.Column(db.String(20), unique=True, nullable=False)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    uploaded_file = db.Column(db.LargeBinary)


class adminpage(ModelView):
    def is_accesible(self):
        access = False
        if 'admin' not in session:
            access = False
            redirect(url_for("login"))
        else:
            access = True
        return access
admin.add_view(adminpage(Users, db.session))
admin.add_view(adminpage(Files, db.session))



@app.route('/', methods=["GET"])
@app.route('/home', methods=["GET"])
def homepage():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    message=None
    if request.method == "POST":
        user = request.form["username"]
        passwd = request.form["password"]
        session['username'] = user
        login = Users.query.filter_by(profile_name=user, profile_passwd=passwd).first()
        if login:
            message = flash(f"Logged In Successfully as {user}", category="success")
            return redirect(url_for("homepage"))
        else:
            message = flash("Check credentials and try again", category="danger")
    return render_template("login.html", message=message)

@app.route("/logout", methods=["GET","POST"])
def logout():
    message=None
    if 'username' not in session:
        message = flash("You are not logged in", category="danger")
    else:
        message = flash("Logged Out", category="success")
        session.pop("username")
        return redirect(url_for('login'))
    return redirect(url_for('login'))
        
@app.route("/register", methods=["GET","POST"])
@app.route("/signup", methods=["GET","POST"])
@app.route("/sign_up", methods=["GET","POST"])
def register():
    message = None
    method = request.method
    if method == "POST":
        mail = request.form["email_address"]
        username = request.form["username"]
        password = request.form["user_pass"]
        conf = request.form["conf_pass"]
        number = request.form["Phone_number"]
        if conf == password:
            try:
                register = Users(profile_name=username, profile_passwd=password, profile_email=mail, profile_number=number)
                db.session.add(register)
                db.session.commit()
                message = flash("Registered Succesfully", category="success")
                return redirect(url_for("login"))
            except:
                flash("User already exists", category="danger")
        else:
            flash("Passwords do not match", category="danger")
    return render_template("register.html", message=message)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload():
    return render_template("upload.html")

@app.route('/uploader', methods=['POST'])
def upload_file():
    # 
    pass
    return render_template("upload.html", message=message)


@app.route('/download')
def download():
    # if session['username'] == 'admin':
    #     files = []
    #     for filename in os.listdir(f'upload/{name}'):
    #         path = os.path.join(f'upload/{name}', filename)
    #         if os.path.isfile(path):
    #             files.append(filename)
    #     name = request.form['']
    pass
    return render_template("download.html", files=files)

# @app.route('/files/<file:file>')
# def file_download(file):
#     """Download a file."""

#     return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

if __name__ == '__main__':
	app.run('0.0.0.0', 80, debug=True)
