from flask import Flask, render_template, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, StringField, validators

app = Flask(__name__)
app.secret_key = "teiSajiepeera8Hieroot8wiel8ahmais5rue3oo"
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text(160), nullable=False)

BookForm = model_form(Book, base_class = FlaskForm, db_session = db.session)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)

class UserForm(FlaskForm):
    email = StringField("email", validators=[validators.email("Please type correct email address.")])    
    password = PasswordField("password", validators=[validators.InputRequired()])

@app.before_first_request
def initDb():
    db.create_all()

    db.session.add(Book(name="Punaisen lokakuun metsästys", description="Sukellusvene lähtee vesille ja kapteeni loikkaa mereen"))
    db.session.commit()

@app.errorhandler(404)
def error404(e):
    error = "Page was not found, please go back to home"
    return render_template("error.html", error = error)

@app.errorhandler(403)
def error403(e):
    error = "Please login first to add or edit the books"
    return render_template("error.html", error = error)


@app.route("/books/edit/<int:id>", methods=["GET", "POST"])
@app.route("/books/add", methods=["GET", "POST"])
def addBook(id=None):
    loginRequired()
    book = Book()
    button = "Add"
    text = "New Book added."

    if id:
        book = Book.query.get_or_404(id)
        button = "Edit"
        text = "Book edited"

    form = BookForm(obj=book)

    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.add(book)
        db.session.commit()
        flash(text)
        return redirect("/")
    
    return render_template("add.html", form = form, button = button)

def currentUser():
    try:
        uid = int(session["uid"])
    except:
        return None

    return User.query.get(uid)

app.jinja_env.globals["currentUser"] = currentUser

def loginRequired():
    if not currentUser():
        abort(403)

@app.route("/books/delete/<int:id>")
def deleteBook(id):
    loginRequired()
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted.")
    return redirect("/")

@app.route("/users/login", methods=["GET", "POST"])
def loginUser():        
    form = UserForm()
    button = "Login"

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Bad username or password, please try again.")
            return redirect("/users/login")   
        if not user.checkPassword(password):
            Flash("Bad username or password, please try again.")
            return redirect("users/login")
        else:
            flash("Login succesfully")
            session["uid"] = user.id
            user2 = currentUser()
            print(user2.email)
            return redirect("/")
    
    return render_template("login.html", form = form, button = button)

@app.route("/users/register", methods=["GET", "POST"])
def registerUser():
    button = "Register me"
    form = UserForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash("User with same email all ready exists!")
            return redirect("/users/register")

        user = User(email = email)
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()
        session["uid"] = user.id
        flash("Thank you, welcome to add books")
        return redirect("/")
    
    return render_template("register.html", form = form, button = button)

@app.route("/users/logout")
def logoutUser():
    if session["uid"]:
        session["uid"] = None
        flash("Successfully logged out.")
        return redirect("/")

    flash("Please login first to logout")
    return redirect("/")

@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books = books)

if __name__ == "__main__":
    app.run()
