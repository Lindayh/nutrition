from flask import Flask, render_template
from models import db, Fruit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fruit_and_veg.db'
db.init_app(app)

vitamins_list = ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin E", "Folat",
                "Vitamin K", "Niancin", "Riboflavin", "Tiamin", "Vitamin B6", "Vitamin B12"]

minerals_list = ["Fosfor","Jod","Järn","Kalcium","Kallium","Magnesium","Salt","Selen","Zink"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mineraler")
def mineraler():
    return render_template("mineraler.html", minerals=minerals_list)

@app.route("/vitaminer")
def vitaminer():
    return render_template("vitaminer.html", vitamins=vitamins_list)

@app.route("/vitaminer/<vitamin>")
def vitamin_info(vitamin):
    if vitamin in vitamins_list:
        return render_template("vitamin_info.html", vitamins = vitamins_list, vitamin=vitamin)
    else:
        return render_template("vitaminer.html", vitamins = vitamins_list)

@app.route("/mineraler/<mineral>")
def mineral_info(mineral):
    if mineral in minerals_list:        
        return render_template("mineral_info.html", minerals=minerals_list, mineral=mineral)
    else:
        return render_template("mineraler.html", minerals=minerals_list)

@app.route("/search")
def search():
    return render_template("search.html") 

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/om")
def about():
    return render_template("about.html")

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")
if __name__ == "__main__":
    app.run(debug=True)
