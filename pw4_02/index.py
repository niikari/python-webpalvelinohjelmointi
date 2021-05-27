from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "ikeph4AhGhahzee5Dei6vaiPhae5na9ezierieL5"
db = SQLAlchemy(app)

class Esine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    esine = db.Column(db.String, nullable=False)
    lainassa = db.Column(db.String, nullable=False)

EsineForm = model_form(Esine, base_class = FlaskForm, db_session = db.session)

@app.before_first_request
def initDb():
    db.create_all()

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
def newBorrow(id=None):
    esine = Esine()
    button = "Vahvista laina"

    if id:
        esine = Esine.query.get_or_404(id)
        button = "Muokkaa lainan tietoja"
    
    form = EsineForm(obj=esine)

    if form.validate_on_submit():
        form.populate_obj(esine)
        db.session.add(esine)
        db.session.commit()
        flash("Laina vahvistettu.")
        return redirect("/")
    
    return render_template("new.html", form=form, button=button)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def deleteBorrow(id):
    esine = Esine.query.get_or_404(id)
    db.session.delete(esine)
    db.session.commit()
    flash("Laina poistettu.")
    return redirect("/")

@app.route("/")
def index():
    esineet = Esine.query.all()
    return render_template("index.html", esineet = esineet)

if __name__ == "__main__":
    app.run()
