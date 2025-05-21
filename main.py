import flet as ft
from api_key import API_KEY2
import requests

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def obtener_clima(ciudad): #función totalmente aparte de la parte gráfica.
    PARAMETROS = {"q":ciudad , "appid":API_KEY2, "lang":"es", "units":"metric"}
    respuesta = requests.get(BASE_URL,PARAMETROS)
    print(respuesta.json())
    if respuesta.status_code == 200:
        info = respuesta.json()
        return {"Ciudad":info["name"],
                "Longitud":info["coord"]["lon"],
                "Latitud":info["coord"]["lat"],
                "Temperatura":info["main"]["temp"],
                "Condiciones":info["weather"][0]["description"],
                "Viento":info["wind"]["speed"],
                "Humedad":info["main"]["humidity"],
                "Temp_min":info["main"]["temp_min"],
                "Temp_max":info["main"]["temp_max"],
        }
            
    else:
        return f"Ocurrio un error {respuesta}"
datos = obtener_clima("Punta Arenas") #se maneja como global
print(datos.get("Humedad"))
#print("datos" in globals())
#print(datos.get("Ciudad"))

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def icono(condiciones):
    iconos = [
        "cielo despejado",
        "pocas nubes",
        "nubes dispersas",
        "nubes rotas",
        "lluvia",
        "lluvia de ducha",
        "tomenta",
        "nieve",
        "niebla"
    ]

def main(page: ft.Page):

    #valores que pongo solo en desarrollo, luego esto se debe borrar
    page.window.width = 360
    page.window.height = 660
    page.window.resizable = False

    #valores que debo usar cuando se lance la aplicacion:
    #ancho = page.window.width
    #alto = page.window.height

    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
   
    #por buena práctica voy a usar funciones y variables privadas como _c o _top que solo deben ser tratadas dentro de la funcion main

    expandido = True #esta variable después la uso como nonlocal para acceder a ella, necesito simular una especie de switch/estados entre clicks (no existe en flet)
    
    #animación
    def _expandir(e):
        nonlocal expandido
        if e.name == "click" and expandido:
            _c.content.controls[0].height=page.window.height*0.80
            _c.content.controls[0].update()
        else:
            _c.content.controls[0].height=page.window.height*0.28
            _c.content.controls[0].update()
        expandido = not expandido

    def _top():
        top = ft.Container(
            width=page.window.width,
            height=page.window.height * 0.28, #28% de la altura
            gradient=ft.LinearGradient(
                begin=ft.alignment.bottom_left,
                end=ft.alignment.top_right,
                colors=["#66add0", "#0e83bf"]
            ),
            border_radius=20,
            animate=ft.Animation(duration=350, curve="decelerate"),
            on_click=lambda e: _expandir(e), #podríamos usar solo _expandir siempre y cuando en la funcion sea : _expandir(e: ft.ControlEvent)
            padding=15,
            margin=5,
            content = ft.Column(
                alignment="start", #solamente para ser explicito, ya que una columna en flet por defecto parte desde arriba.
                spacing=10,
                controls=[
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.Text(datos.get("Ciudad"),
                                    size=15,
                                    weight = "W_700",                                    
                                    color=ft.Colors.WHITE),                           
                        ]
                    ),
                    # ft.Container(
                    #     padding=ft.padding.only(bottom=20)
                    # ),
                    ft.Row(
                        alignment="center",
                        spacing=20,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Container( #contenedores ofrecen mas decoradores, a diferencia de row o column que son como layouts                                     
                                        width=120,
                                        height=120,
                                        content=ft.Image(src="weezle-cloud-sun.png"),                                       
                                    )
                                ]
                            ),
                            ft.Column(
                                spacing=5,
                                horizontal_alignment="center",
                                controls=[
                                    ft.Text(
                                        "Hoy",
                                        color=ft.Colors.WHITE,
                                        size=14,
                                        #text_align="center",
                                    ),
                                    ft.Row(
                                        alignment="center",
                                        spacing=0,
                                        controls=[
                                            ft.Container(
                                                content=ft.Text(
                                                    int(datos.get("Temperatura")),
                                                    size=40,
                                                )
                                            ),
                                            ft.Container(
                                                content=ft.Text(
                                                    "°",
                                                    size=40,
                                                )
                                            )
                                        ]
                                    ),
                                    ft.Text(
                                        datos.get("Condiciones"),
                                        size=14,
                                        color=ft.Colors.WHITE,
                                    )   
                                ]
                            ),                         
                        ]

                    ),
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.Container(
                                width=200,
                                height=2,
                                bgcolor=ft.Colors.BLACK,
                                opacity=0.3,
                            )
                        ]
                        
                        
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.Container(
                                width=120,
                                height=120,
                                padding=5,
                                border=ft.border.all(3),
                                content=ft.Text("Contenedor1"),
                            ),
                            ft.Container(
                                width=120,
                                height=120,
                                padding=5,
                                border=ft.border.all(3),
                                content=ft.Text("Contenedor2"),
                            ),
                        ]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.Container(
                                width=200,
                                height=200,
                                padding=50,
                                border=ft.border.all(3),
                                content=ft.Text("Contenedor3"),
                            )
                        ]
                    ),
                    ft.Row(
                        alignment="center",
                        controls=[
                            ft.Text(
                                "Fila3"
                            )
                        ]
                    )

                ]
                
            )
        )
        return top

    _c = ft.Container(
        #width=310,
        #height=660,
        expand=True,
        border_radius=25,
        bgcolor="black",
        padding=5,
        content=ft.Stack(controls=[_top()]),
                
    )
    page.add(_c)



if __name__ == "__main__" : #aunque no es necesario con tan poco código y sabemos que vamos usar un solo fichero, si es una buena práctica
    ft.app(target=main, assets_dir = "images")

