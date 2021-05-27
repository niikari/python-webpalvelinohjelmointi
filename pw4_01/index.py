from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "kah9jo2uch2hiegahWai4iengavai5"
db = SQLAlchemy(app)

class Asiakas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String, nullable=False)
    sukunimi = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    puhelin = db.Column(db.String, nullable=False)

AsiakasForm = model_form(Asiakas, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initDb():
    db.create_all()

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@app.route("/add", methods=["GET", "POST"])
def addNew(id=None):
    asiakas = Asiakas()
    button = "Lisää uusi."
    if id:
        button = "Muokkaa halutuksi."
        asiakas = Asiakas.query.get_or_404(id)
    
    form = AsiakasForm(obj=asiakas)

    if form.validate_on_submit(): # m
        form.populate_obj(asiakas)
        db.session.add(asiakas)
        db.session.commit()
        if id:
            flash("Asiakasta muokattu onnistuneesti.")
        else:        
            flash("Asiakas lisätty onnistuneesti.")
        return redirect("/")
    
    return render_template("new.html", form = form, button = button)

@app.route("/delete/<int:id>")
def deleteOne(id):
    asiakas = Asiakas.query.get_or_404(id)
    db.session.delete(asiakas)
    db.session.commit()
    flash("Asiakas poistettu onnistuneesti.")
    return redirect("/")

@app.route("/")
def index():
    asiakkaat = Asiakas.query.all()
    return render_template("index.html", asiakkaat=asiakkaat)

if __name__=="__main__":
    app.run()
