from flask import Flask

app = Flask(__name__)

from app import routes  # Importation des routes après la création de l'app
