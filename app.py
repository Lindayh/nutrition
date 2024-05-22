from flask import Flask, render_template
from models import db, Fruit
from minerals_info import minerals_info


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fruit_and_veg.db'
db.init_app(app)

vitamins_list = ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin E", "Folat", "Vitamin K", "Niancin", "Riboflavin", "Tiamin", "Vitamin B6", "Vitamin B12"]

minerals_list = ["Fosfor","Jod","Järn","Kalcium","Kalium","Magnesium","Natrium","Selen","Zink"]

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
    mineral_info = next((mineral_name for mineral_name in minerals_info if mineral_name["name"]==mineral), None)
    
    mineral_mapping = {
    "Fosfor": "Fosfor_mg",
    "Jod": "Jod_mikrog",
    "Järn": "Järn_mg",
    "Kalcium": "Kalcium_mg",
    "Kalium": "Kalium_mg",
    "Magnesium": "Magnesium_mg",
    "Natrium": "Natrium_mg",
    "Selen": "Selen_mikrog",
    "Zink": "Zink_mg",
    "Vitamin B6": "Vitamin_B6_mg",
    "Vitamin B12": "Vitamin_B12_mikrog"
    }
    column_name = mineral_mapping.get(mineral)

    top_fruits = Fruit.query.order_by(getattr(Fruit, column_name).desc()).limit(10).all()

    return render_template("mineral_info.html", minerals=minerals_list, mineral=mineral_info, top_fruits=top_fruits)

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
