from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "eeraep5ien2EH7MaeZahyei9phuthe"
db = SQLAlchemy(app)

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.Text, nullable=False)
    tweeter = db.Column(db.String, nullable=False)

TweetForm = model_form(Tweet, base_class = FlaskForm, db_session = db.session)

@app.before_first_request
def atFirst():
    db.create_all()

@app.route("/tweet", methods=["GET", "POST"])
def tweet():
    form = TweetForm()

    if form.validate_on_submit():
        tweet = Tweet()
        form.populate_obj(tweet)
        db.session.add(tweet)
        db.session.commit()
        flash("Just twiited!")
        return redirect("/")
        
    return render_template("tweet.html", form = form)

@app.route("/")
def index():
    tweets = Tweet.query.all()
    return render_template("index.html", tweets = tweets)

if __name__ == "__main__":
    app.run()
