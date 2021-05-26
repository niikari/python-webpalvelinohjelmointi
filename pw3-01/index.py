from flask import Flask, render_template, flash, redirect

app = Flask(__name__)
app.secret_key = "ahpaghu3ohcouFuaYi3Quaevaineihashieko4mu"

@app.route("/first")
def first():
    flash("This message is from first page! WTF?!")
    return redirect("/")
    
@app.route("/second")
def second():
    flash("This message is from second page! You are welcome!")
    return redirect("/")

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run()
