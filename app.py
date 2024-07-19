from flask import Flask, render_template, request, redirect
from models import db, Fruit
from info import RDI_list_vit, RDI_list_min, minerals_info, vitamins_info, veg_fruit_info
from googletrans import Translator
import requests
import os
from dotenv import load_dotenv


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fruit_and_veg.db'
db.init_app(app)

project_folder = os.path.expanduser('~/nutrition')
load_dotenv(os.path.join(project_folder, '.env'))

vitamins_list = ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin E", "Folat", "Vitamin K", "Niacin", "Riboflavin", "Tiamin", "Vitamin B6", "Vitamin B12"]

minerals_list = ["Fosfor","Jod","Järn","Kalcium","Kalium","Magnesium","Natrium","Selen","Zink"]

vitamin_mapping = {
    "Vitamin_A_RE_per_mikrog": "Vitamin A",
    "Vitamin_C_mg": "Vitamin C",
    "Vitamin_D_mikrog": "Vitamin D",
    "Vitamin_E_mg": "Vitamin E",
    "Folat_mikrog": "Folat",
    "Vitamin_K_mikrog": "Vitamin K",
    "Niacin_mg": "Niacin",
    "Riboflavin_mg": "Riboflavin",
    "Tiamin_mg": "Tiamin",
    "Vitamin_B6_mg": "Vitamin B6",
    "Vitamin_B12_mikrog": "Vitamin B12"
}

mineral_mapping = {
    "Fosfor_mg": "Fosfor",
    "Jod_mikrog": "Jod",
    "Järn_mg": "Järn",
    "Kalcium_mg": "Kalcium",
    "Kalium_mg": "Kalium",
    "Magnesium_mg": "Magnesium",
    "Natrium_mg": "Natrium",
    "Selen_mikrog": "Selen",
    "Zink_mg": "Zink",
}

nutrient_mapping = {**mineral_mapping, **vitamin_mapping}

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

    for index,col_name in enumerate(column_names):
        if col_name.startswith(vitamin_) or col_name.startswith(vitamin):
            data = []

            if col_name=="Niacin_mg" or col_name=="Niacinekvivalenter_NE_per_mg":
                top_10 = Fruit.query.order_by((getattr(Fruit, "Niacinekvivalenter_NE_per_mg")).desc()).limit(10).all()
            else:
                top_10 = Fruit.query.order_by((getattr(Fruit, col_name)).desc()).limit(10).all()

            if "mg" in col_name.split("_"): unit = f"{vitamin} (mg)"
            if "mikrog" in col_name.split("_"): unit = f"{vitamin} (mikrog)"

            for idx, vitamin_dict in enumerate(vitamins_info):
                vit_dict_name = vitamin_dict['name']

                if vit_dict_name == vitamin:
                    vitamin_text = []
                    for key in vitamin_dict:
                        if key!="name":
                            vitamin_text.append(vitamin_dict[key])

            for index,fruit_cls in enumerate(top_10):
                temp_dict = {"name" : fruit_cls.Namn,
                             "vitamin_value" : getattr(fruit_cls, col_name),
                             "unit": unit}

                if vitamin == "Vitamin A":
                    temp_dict = {"name" : fruit_cls.Namn,
                             "vitamin_value" : getattr(fruit_cls, col_name),
                             "unit": "Vitamin A (Retinolekvivalenter per mikrogram)"}

                if vitamin == "Niacin":
                    temp_dict = {"name" : fruit_cls.Namn,
                             "vitamin_value" : getattr(fruit_cls, "Niacinekvivalenter_NE_per_mg"),
                             "unit": "Niacin (Niacinekvivalenter per mg)"}

                data.append(temp_dict)

            if vitamin in RDI_list_vit.keys():
                vitamin_RDI = RDI_list_vit[vitamin]


            return render_template("vitamin_info.html", vitamins = vitamins_list, vitamin=vitamin, top_10=data, vitamin_text=vitamin_text, vitamin_RDI=vitamin_RDI)


    if vitamin in vitamins_list:
        return render_template("vitamin_info.html", vitamins = vitamins_list, vitamin=vitamin)
    else:   # Prevent user to create random path. E.g. vitaminer/blabla
        return render_template("vitaminer.html", vitamins = vitamins_list)

@app.route("/mineraler/<mineral>")
def mineral_info(mineral):
    mineral_info = next((mineral_name for mineral_name in minerals_info if mineral_name["name"]==mineral), None)

    for idx, key in enumerate(mineral_mapping):
        value = mineral_mapping[key]
        if mineral == value:
            column_name = key

    top_fruits = Fruit.query.order_by(getattr(Fruit, column_name).desc()).limit(10).all()

    if mineral in RDI_list_min.keys():
        mineral_RDI = RDI_list_min[mineral]

    return render_template("mineral_info.html", minerals=minerals_list, mineral=mineral_info, top_fruits=top_fruits, mineral_RDI=mineral_RDI)

@app.route("/search")
def search():
    search_query = request.args.get("search")
    query_result_list = False
    page = request.args.get('page', 1, type=int)

    if search_query:
        query = Fruit.query.filter(
                                        Fruit.Namn.startswith(search_query.title()) |
                                        Fruit.Namn.contains(f'%{search_query.lower()}%')
                                            )
        query_result = query.all()

        query_result_list = list(set(sorted(query_result, key= lambda x: x.Namn, reverse=True)))

        if int(query.count()) == 1:
            item_name = query_result_list[0].__getattribute__('Namn')
            return redirect(f"/{item_name}")

        if int(query.count()) >10:
            paged_query = query.paginate(page=page, per_page=10, error_out=False)

            return render_template('search.html', results=paged_query, search=search_query, page=page)

        return render_template('search.html', results=query_result_list, page=page)

    return render_template("search.html", results=query_result_list)

@app.route("/<item>")
def item_page(item):

    query = Fruit.query.filter(Fruit.Namn.like(item)).first()

    print(f'Item: {item}, query: {query}')

    if query==None:
        return render_template('search.html', not_page=True)
    else:
        query = query.__dict__

        query = {key: value for key, value in query.items() if value is not None}

        del query['_sa_instance_state']
        del query['Namn']


        for index,key in enumerate(veg_fruit_info):
            name = veg_fruit_info[index]['titel']
            if name == item:
                fact = veg_fruit_info[index]['fakta'] 
                img = veg_fruit_info[index]['bild']

        data = { 'name' : item,
                'object' : query,
                'vitamins' : vitamin_mapping,
                'minerals' : mineral_mapping,
                'fact' : fact,
                'img' : img
                }

        return render_template("search.html", searched_page=data)

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/om")
def about():
    return render_template("about.html")

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")


# @app.route('/img_dump')
# def imgs_test():
#     return render_template('__.html', _dict = veg_fruit_info)

if __name__ == "__main__":
    app.run(debug=True)
