"""
This is the solution for the Globant Exercise PokeBerries

Classes:
    
    Berry

Functions:

    main

"""
from typing import Any
import os
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.testclient import TestClient
import orjson
from dotenv import load_dotenv
import httpx
import numpy as np


app = FastAPI()
load_dotenv()    #reads the environment variables from the . env file
url = os.getenv('URL')

client = TestClient(app)  #TestClient's object for testing


class CustomORJSONResponse(Response):
    """
    A Custom Response.
   
    """
    
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)



@app.get('/allBerryStats', response_class=CustomORJSONResponse)
async def main():
    """     
    Use this endpoint https://pokeapi.co/api/v2/berry/ to calculate poke-berries statistics
    
    Return: Json object containing poke-berries statistics: berries_names, min_growth_time, median_growth_time,
    max_growth_time, variance_growth_time, mean_growth_time and frequency_growth_time.

    """

    count = httpx.Client().get(url).json()['count']
    names = []
    growth_times = []

    async for berry in Berry(count):
        names.append(berry.json()['name'])
        growth_times.append(berry.json()['growth_time'])

    n_array = np.array(growth_times)
    frecuency = dict()
    unique_values, count_ = np.unique(n_array, return_counts=True)
   
    for key, value in zip(unique_values, count_):
        frecuency[str(key)] = int(value)

    data = {
            "berries_names": names,
            "min_growth_time": int(min(growth_times)),
            "median_growth_time": float(np.median(n_array)),
            "max_growth_time": int(max(growth_times)),
            "variance_growth_time": float(np.var(n_array)),
            "mean_growth_time": float(np.mean(n_array)),
            "frequency_growth_time": frecuency
           }

    return data

    
    
def test_main():
    response = client.get('/allBerryStats')
    assert response.status_code == 200


class Berry:
    """
    A Iterator class to represent a berry.
    
    ...

    Atributes
    ---------

    count: number of berries
    _index: variable to control the number of berries

    Method
    ------
    aiter():
        One of two methods to implement an async iterator
    anext():
        One of two methods to implement an async iterator

    """
    def __init__(self, count) -> None:
        self._count = count
        self._index = 1

    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self._index <= self._count:
            async with httpx.AsyncClient() as client:
                response = await client.get(url+str(self._index))
                self._index += 1
                return response
        else:
             raise StopAsyncIteration
        
