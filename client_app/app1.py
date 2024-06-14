from handler import CONFIGURATION, create_app

app = create_app(5001, 'shared1')

if __name__ == "__main__":
    app.run(port=CONFIGURATION.PORT, debug=CONFIGURATION.DEBUG)
