from flask import Flask, render_template
from models import db, Fruit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fruit_and_veg.db'
db.init_app(app)

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

@app.route("/test")
def test():
    frukter=Fruit.query.order_by(Fruit.Vitamin_A_RE_per_mikrog.desc()).limit(10).all()
    return render_template('test.html', frukter=frukter)

if __name__ == "__main__":
    app.run(debug=True)
