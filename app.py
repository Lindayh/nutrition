from flask import Flask, render_template, request
from models import db, Fruit
from minerals_info import minerals_info
from vitamins_info import vitamins_info
from RDI_info import RDI_list_vit, RDI_list_min
from fakta_info import veg_fruit_info, get_fact
import requests
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fruit_and_veg.db'
db.init_app(app)

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

        #region Vitamin top 10
    for index,col_name in enumerate(column_names):
        if col_name.startswith(vitamin_) or col_name.startswith(vitamin):
            data = []
            print(f"Column name: {col_name}")

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
            #endregion

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

    column_name = mineral_mapping.get(mineral)

    top_fruits = Fruit.query.order_by(getattr(Fruit, column_name).desc()).limit(10).all()

    if mineral in RDI_list_min.keys():
        mineral_RDI = RDI_list_min[mineral]

    print(mineral)
    return render_template("mineral_info.html", minerals=minerals_list, mineral=mineral_info, top_fruits=top_fruits, mineral_RDI=mineral_RDI)

@app.route("/search")
def search():
    search_query = request.args.get("search")
    query_result = False

    if search_query:

        query_result = []

        query_result.extend( Fruit.query.filter(func.lower(getattr(Fruit,'Namn')).startswith(search_query.title()) ).all()  )
        query_result.extend( Fruit.query.filter(func.lower(getattr(Fruit,'Namn')).contains(f'%{search_query.lower()}%')).all()  )

        query_result = list(set(sorted(query_result, key= lambda x: x.Namn, reverse=True)))

        print(type(query_result))

        return render_template('search.html', results=query_result)

    return render_template("search.html", results=query_result)
    # if not search_query:
    #     return render_template("search.html")

    # check = Fruit.query.filter(Fruit.Namn.startswith(search_query)).first()

    # if check:
    #     query_name = check.Namn
    #     api_query = requests.get(f"https://sv.wikipedia.org/api/rest_v1/page/summary/{query_name}")
    #     api_data = api_query.json()
    #     api_image = api_data.get("thumbnail", {}).get("source")

    #     if not api_image:
    #         query_name = check.Namn

    #     fact_data = get_fact(veg_fruit_info, check.Namn)

    #     if isinstance(fact_data, tuple):
    #         fact, img = fact_data
    #     else:
    #         fact = fact_data
    #         img = None

    #     filtered_data = {}
    #     print(api_data)
    #     for nutrient_name, column_name in nutrient_mapping.items():
    #         value = getattr(check, column_name)
    #         if isinstance(value, (int, float)) and value > 0:
    #             if nutrient_name not in filtered_data:
    #                 filtered_data[nutrient_name] = []
    #             filtered_data[nutrient_name].append(value)
    #     return render_template("search.html", results=filtered_data, query_name=query_name, message=None, fact=fact, img=img, api_image=api_image)

    # else:
    #     return render_template("search.html", message="Ingen sökträff hittades.")


@app.route("/<item>")
def item_page(item):

    query = Fruit.query.filter(Fruit.Namn==item).first()
    query = query.__dict__

    if query==None:
        return render_template('search.html', not_page=True)

    print(f'Query result: {query['Namn']} | item: {item}')

    query = {key: value for key, value in query.items() if value is not None}



    del query['_sa_instance_state']
    del query['Namn']

    img = '../static/images/placeholder.png'


    for index,key in enumerate(veg_fruit_info):
        name = veg_fruit_info[index]['titel']
        if name == item:
            fact = veg_fruit_info[index]['fakta']

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

if __name__ == "__main__":
    app.run(debug=True)
