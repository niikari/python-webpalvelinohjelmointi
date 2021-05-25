from flask import Flask, render_template
app = Flask(__name__)

@app.route("/index")
def index():
    muuttuja = "tämä tulee index funktiosta"
    return render_template("index.html", muuttuja=muuttuja)

@app.route("/other")
def other():
    muuttuja = "tämä tulee other funktiosta"
    return render_template("other.html", muuttuja=muuttuja)

if __name__=="__main__":
    app.run()