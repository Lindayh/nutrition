from flask import Flask, render_template
from models import db, Fruit
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fruit_and_veg.db'
db.init_app(app)

vitamins_list = ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin E", "Folat", "Vitamin K", "Niacin", "Riboflavin", "Tiamin", "Vitamin B6", "Vitamin B12"]

minerals_list = ["Fosfor","Jod","Järn","Kalcium","Kalium","Magnesium","Salt","Selen","Zink"]

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
    vitamin_ = vitamin.replace(" ",'_')

    table = Fruit.__table__
    column_names = [column.name for column in table.columns]

    for index,value in enumerate(column_names):
        if value.startswith(vitamin_) or value.startswith(vitamin):
            data = []
            print(f"Column name: {value}")

            if value=="Niacin_mg" or value=="Niacinekvivalenter_NE_per_mg":
                top_10 = Fruit.query.order_by((getattr(Fruit, "Niacinekvivalenter_NE_per_mg")).desc()).limit(10).all()
            else:
                top_10 = Fruit.query.order_by((getattr(Fruit, value)).desc()).limit(10).all()  


            if "mg" in value.split("_"): unit = f"{vitamin} (mg)"
            if "mikrog" in value.split("_"): unit = f"{vitamin} (mikrog)"

            for index,val in enumerate(top_10):
                temp_dict = {"name" : val.Namn,
                             "vitamin_value" : getattr(val, value),
                             "unit": unit}
                
                if vitamin == "Vitamin A":
                    temp_dict = {"name" : val.Namn,
                             "vitamin_value" : getattr(val, value),
                             "unit": "Vitamin A (Retinolekvivalenter per mikgrogram)"}
                
                if vitamin == "Niacin":
                    temp_dict = {"name" : val.Namn,
                             "vitamin_value" : getattr(val, "Niacinekvivalenter_NE_per_mg"),
                             "unit": "Niacin (Niacinekvivalenter per mg)"}

                data.append(temp_dict)
            return render_template("vitamin_info.html", vitamins = vitamins_list, vitamin=vitamin, top_10=data)


    

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
