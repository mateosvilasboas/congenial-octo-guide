import requests
import json
from utils import PlatformLoader, AllPlatformsLoader
from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return """
    <p>Nome do candidato: Mateus Campos Vilasboas Dantas</p>
    <p>Email: mateuscamposdantas@gmail.com</p>
    <p>LinkedIn: <a href="https://www.linkedin.com/in/mateus-campos-vilasboas-dantas/">https://www.linkedin.com/in/mateus-campos-vilasboas-dantas/</a></p>
    """

@app.route("/<platform>/", methods=['GET'])
def show_platform(platform):
    try:
        platform = PlatformLoader(platform=platform)
        platform.get_insights()
        platform.generate_csv(summary=False)
        return 'success', 200
    except Exception as e:
        error = e.args[0]
        return error, 500

@app.route("/<platform>/resumo", methods=['GET'])
def show_platform_summary(platform):
    try:
        platform = PlatformLoader(platform=platform)
        platform.get_insights()
        platform.generate_csv(summary=True)
        return 'success', 200
    except Exception as e:
        error = e.args[0]
        return error, 500

@app.route("/geral/", methods=['GET'])
def show_all():
    try:
        all_platforms = AllPlatformsLoader()
        all_platforms.get_insights()
        all_platforms.generate_csv(summary=False)
        return 'success', 200
    except Exception as e:
        error = e.args[0]
        return error, 500

@app.route("/geral/resumo")
def show_all_summary():
    all_platforms = AllPlatformsLoader()
    all_platforms.get_insights()
    all_platforms.generate_csv(summary=True)
    return 'success', 200
    try:
        all_platforms = AllPlatformsLoader()
        all_platforms.get_insights()
        all_platforms.generate_csv(summary=True)
        return 'success', 200
    except Exception as e:
        error = e.args[0]
        return error, 500