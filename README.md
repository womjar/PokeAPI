Globant Exercise PokeBerries - PokeAPI

In an IDE with Python installed (3.10+), create a virtual environment and copy the following files into it:

(1) berries.py 
(2) .env 
(3) requirements.txt

WARNING: Be careful when download the configuration file .env

Next, run the following command: pip install -r requirements.txt, then run:

uvicorn berries:app

Finally, enter the following URL in a browser: http://127.0.0.1:8000/allBerryStats
