from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from calorie import Calorie
from temperature import Temperature

""" Si corremos esta hoja solo con la primera línea phyton importará el script pero
también ejecutará el archivo temperature.py dentro de flask_app-py.
 Esto sucede siempre que importas un script de otro script. 
 Para evitarlo se escribe en el .py importado lo siguiente:
   if __name__ == "__main__":
   Ahora si corremos flask_app.py no ocurrirá nada, importa la clase pero no la ejecuta.
   Solamente lo ejecutara si es el main script, "__main__" == "__main__", en esta hoja
    el __name__ es temperatura y por eso no se ejecuta
    
    En otras palabras si el script es importado desde algún lugar este no se inicializara"""


# Creamos instancia de aplicación Flask
app = Flask(__name__)


class HomePage(MethodView):

    def get(self):
        return render_template("index.html")

class CaloriesFormPage(MethodView):

# Tiene el get para ejecutar y mostrar el formulario

    def get(self):
        calories_form = CaloriesForm()

        return render_template("calories_form_page.html", caloriesform=calories_form)

# En el post al CaloriesForm tenemos que darle el argumento (request.form)

    def post(self):
        calories_form = CaloriesForm(request.form)

        temperature = Temperature(country=calories_form.country.data,
                                  city=calories_form.city.data).get()

        calorie = Calorie(weight=float(calories_form.weight.data),
                          height=float(calories_form.height.data),
                          age=float(calories_form.age.data),
                          temperature=temperature)

        calories = calorie.calculate()

# El result=True, permite que el texto que configuramos en el .html solo se vea al enviar el formulario
        return render_template("calories_form_page.html",
                               caloriesform=calories_form,
                               calories=calories,
                               result=True)

class CaloriesForm(Form):
    weight = StringField("Weight: ", default=70)
    height = StringField("Height: ", default=175)
    age = StringField("Age: ", default=32)
    country = StringField("Country: ", default="USA")
    city = StringField("City: ", default="San Francisco")
    button = SubmitField("Calculate")


app.add_url_rule("/", view_func=HomePage.as_view("home_page"))
app.add_url_rule("/calories_form", view_func=CaloriesFormPage.as_view("calories_form_page"))

app.run(debug=True)
