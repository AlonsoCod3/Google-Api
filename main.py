import os
import sheets
from router.products.products_hook import routing

# API
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

sheets.initcializacion()

@app.route('/', methods=['GET'])
def index():
  return "HOLA"

app.register_blueprint(routing, url_prefix="/products")

if __name__ == '__main__':  
  app.run(host='0.0.0.0')