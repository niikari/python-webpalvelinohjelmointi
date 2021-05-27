from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key="iepahB2ji9xao2mie3Ithohquioquo"
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg = db.Column(db.String, nullable=False)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    modyear = db.Column(db.Integer, nullable=False)    

CarForm = model_form(Car, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initDb():
    db.create_all()

@app.route("/add", methods=["GET", "POST"])
def addCar():
    form = CarForm()

    if form.validate_on_submit(): # m
        car = Car()
        form.populate_obj(car)
        db.session.add(car)
        db.session.commit()
        flash("Car added succesfully!")
        return redirect("/")
    
    return render_template("add.html", form=form)

@app.route("/")
def index():
    cars = Car.query.all()
    return render_template("index.html", cars=cars)

if __name__ == "__main__":
    app.run()
