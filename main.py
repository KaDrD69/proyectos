import flet as ft
from api_key import API_KEY2
import requests

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def obtener_clima(ciudad):
    PARAMETROS = {"q":ciudad , "appid":API_KEY2, "units":"metric"}
    respuesta = requests.get(BASE_URL,PARAMETROS)
    if respuesta.status_code == 200:
        info = respuesta.json()
        return {"Ciudad":info["name"],
                "Longitud":info["coord"]["lon"],
                "Latitud":info["coord"]["lat"],
                "Temperatura":info["main"]["temp"],
                "Condiciones":info["weather"][0]["main"],
                "Viento":info["wind"]["speed"]
        }
            
    else:
        return f"Ocurrio un error {respuesta}"

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    
    #por buena práctica voy a usar funciones y variables privadas como _c o _top que solo deben ser tratadas dentro de la funcion main

    def _expandir(e: ft.ControlEvent):
        estado = {"estado": True}        
        if e.name == "click" and estado["estado"]:
            _c.content.controls[0].height=560
            _c.content.controls[0].update()
        else:
            _c.content.controls[0].height=660 * 0.4
            _c.content.controls[0].update()
        estado["estado"] = not estado["estado"]
    
    def _top():
        top = ft.Container(
            width=300,
            height=660 * 0.40, #40% de la altura
            gradient=ft.LinearGradient(
                begin=ft.alignment.bottom_left,
                end=ft.alignment.top_right,
                colors=["#ff6600", "#ffcc00"]
            ),
            border_radius=10,
            animate=ft.Animation(duration=350, curve="decelerate"),
            on_click=_expandir #podría usar lambda e: _expandir(e) en caso de def _expandir(e)
        )
        return top


    _c = ft.Container(
        width=310,
        height=660,
        border_radius=25,
        bgcolor="black",
        padding=5,
        content=ft.Stack(width = 300, height = 550, controls=[_top()]),
                
    )
    page.add(_c)



if __name__ == "__main__" : #aunque no es necesario con tan poco código y sabemos que vamos usar un solo fichero, si es una buena práctica
    ft.app(target=main, assets_dir = None)