from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
     muuttuja = "sana"
     return render_template("index.html", sana=muuttuja)

if __name__=="__main__":
    app.run()

    
