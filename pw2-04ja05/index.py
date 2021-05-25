from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    tulos = ""
    if "first" in request.form and "second" in request.form:
        eka = int(request.form["first"])
        toka = int(request.form["second"])
        tulos = eka * toka        
    return render_template("index.html", tulos=tulos)

if __name__=="__main__":
    app.run()