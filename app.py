import requests
import json
from utils import get_insights, generate_csv
from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return """
    <p>Nome do candidato: Mateus Campos Vilasboas Dantas</p>
    <p>Email: mateuscamposdantas@gmail.com</p>
    <p>LinkedIn: <a href="https://www.linkedin.com/in/mateus-campos-vilasboas-dantas/">https://www.linkedin.com/in/mateus-campos-vilasboas-dantas/</a></p>
    """

@app.route("/<platform>/", methods=['POST'])
def show_platform(platform):
    try:
        data = get_insights(platform=platform)
        generate_csv(data, summary=False)
        return 'success', 200
    except Exception as e:
        error = e.args[0]
        return error, 500

@app.route("/<platform>/resumo", methods=['POST'])
def show_platform_summary(platform):
    try:
        data = get_insights(platform=platform)
        generate_csv(data, summary=True)
        return 'success', 200
    except Exception as e:
        error = e.args[0]
        return error, 500

@app.route("/geral/")
def show_all():
    pass

@app.route("/geral/resumo")
def show_all_summary():
    pass