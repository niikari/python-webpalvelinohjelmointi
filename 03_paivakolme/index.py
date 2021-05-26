from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = "caif0Iengiu7Zuzuaghouh9sae5fiy"

class Mobile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)

@app.before_first_request
def first():
    db.create_all()

MobileForm = model_form(Mobile, base_class = FlaskForm, db_session = db.session)

@app.route("/msg")
def msg():
    flash("New nice flash message!")
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def index():
    form = MobileForm()
    return render_template("index.html", form=form)

if __name__=="__main__":
    app.run()
