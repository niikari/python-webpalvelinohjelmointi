from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)

@app.before_first_request
def first():
    db.create_all()

    car = Car(make="Skoda", model="Fabia")
    db.session.add(car) 

    car = Car(make="Volkswagen", model="Golf")
    db.session.add(car)

    db.session.commit()   

@app.route("/")
def index():
    cars = Car.query.all()
    print(cars)
    return render_template("index.html", cars=cars)

if __name__ == "__main__":
    app.run()