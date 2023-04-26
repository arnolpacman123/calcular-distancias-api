from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from typing import Dict

from geopy import distance


def calcular_distancia(punto1, punto2):
    """Función para calcular la distancia entre dos puntos"""
    return distance.distance(punto1, punto2).meters


def obtener_diccionario_y_punto_mas_cercanos(lista_diccionarios, punto_dado):
    """Función para obtener el diccionario y el punto más cercanos a un punto dado en una lista de diccionarios"""
    diccionario_mas_cercano = None
    punto_mas_cercano = None
    distancia_minima = float('inf')

    punto_dado = (punto_dado['lat'], punto_dado['lng'])

    for diccionario in lista_diccionarios:
        path = diccionario['options']['path']
        for punto_path in path:
            punto = (punto_path['lat'], punto_path['lng'])
            distancia = calcular_distancia(punto_dado, punto)
            if distancia < distancia_minima:
                distancia_minima = distancia
                diccionario_mas_cercano = diccionario
                punto_mas_cercano = {
                    'lat': punto_path['lat'],
                    'lng': punto_path['lng']
                }

    return diccionario_mas_cercano, punto_mas_cercano


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/find_closest_polyline_and_point")
async def find_closest_polyline_and_point(data: Dict):
    polylines = data["polylines"]
    point = data["point"]
    diccionario_mas_cercano, punto_mas_cercano = obtener_diccionario_y_punto_mas_cercanos(
        polylines,
        point
    )

    return {"polyline": diccionario_mas_cercano, "point": punto_mas_cercano}
