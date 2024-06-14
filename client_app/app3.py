from handler import CONFIGURATION, create_app

app = create_app(5003, 'shared3')

if __name__ == "__main__":
    app.run(port=CONFIGURATION.PORT, debug=CONFIGURATION.DEBUG)
