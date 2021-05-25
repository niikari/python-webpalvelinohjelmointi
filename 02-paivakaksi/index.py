from flask import Flask, render_template
app = Flask(__name__)

@app.route("/index")
def index():
    list = ["omena", "päärynä", "porkkana"]
    return render_template("index.html", list=list)

if __name__ == "__main__":
    app.run()