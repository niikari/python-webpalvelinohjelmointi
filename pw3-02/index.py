from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = "ohr8ach9de2peey4aigo6ieLahfee7"

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String)
    done = db.Column(db.Boolean, nullable=False)

TodoForm = model_form(Todo, base_class = FlaskForm, db_session = db.session)

@app.before_first_request
def atFirst():
    db.create_all()
    db.session.add(Todo(todo="Imurointi", done=False))
    db.session.add(Todo(todo="Pyykkien pesu", done=False))
    db.session.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    form = TodoForm()
    todos = Todo.query.all()
    return render_template("index.html", form = form, todos=todos)

if __name__=="__main__":
    app.run()
