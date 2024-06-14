from flask import Flask
from handler.config import Config
from handler.view import services

app = Flask(__name__)

app.register_blueprint(services)

if __name__ == '__main__':
    app.run(port=Config.PORT, debug=Config.DEBUG)
