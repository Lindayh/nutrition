from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vitaminer")
def vitaminer():
    return render_template("vitaminer.html")

@app.route("/mineraler")
def mineraler():
    return render_template("mineraler.html")

@app.route("/search")
def search():
    return render_template("search.html") 

@app.route("/team")
def team():
    return render_template("team.html")

if __name__ == "__main__":
    app.run(debug=True)
