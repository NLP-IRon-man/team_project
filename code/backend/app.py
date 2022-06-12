from flask import Flask
from backend.blueprints.blueprints import blueprint_home, blueprint_movie

app = Flask(__name__)
app.register_blueprint(blueprint_home)
app.register_blueprint(blueprint_movie)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
