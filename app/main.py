from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from .db import db


ORIGINS = [
    '*'
    # "http://devmaps.xyz",
    # "https://devmaps.xyz",
    # "http://localhost",
    # "http://localhost:8080",
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(lng: str, lat: str):

    sql = f"""
        SELECT
              fips AS fip
            , ST_X(ST_Centroid(geom)) AS lng
            , ST_Y(ST_Centroid(geom)) AS lat
            , name AS county
            , state_name
            , ST_Distance_Sphere(Point({lng}, {lat} ),ST_Centroid(geom)) AS dist
            , population AS min_price 
            , ST_AsGeoJSON(geom) as geojson
        FROM
            counties
        WHERE
            ST_Contains( ST_MakeEnvelope(
            Point(({lng} + (200 / 111)),({lat} + (200 / 111))),
            Point(({lng} - (200 / 111)),({lat} - (200 / 111)))
            ),	geom )
        ORDER BY
            dist
        LIMIT 8;
    """
    data = db.mysql_select(sql)

    for item in data:
        json_data = item['geojson']
        item['geojson'] = json.loads(json_data)

    return data
