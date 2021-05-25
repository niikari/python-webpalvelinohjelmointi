from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    lista = ["päärynä", "omena", "banaani", "sipuli", "sipulikeitto", "täähän vois olla ruokalista"]
    return render_template("index.html", lista = lista)

if __name__=="__main__":
    app.run()