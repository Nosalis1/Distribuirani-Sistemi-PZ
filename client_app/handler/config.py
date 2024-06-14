class Config:
    DEBUG = True
    TESTING = False
    SERVER_PORT = 5000
    SERVER_ADDRESS = "http://127.0.0.1:" + str(SERVER_PORT)

    def __init__(self, port, shared_dir="./shared1"):
        self.PORT = port
        self.ADDRESS = "http://127.0.0.1:" + str(port)
        self.SHARED_DIR = shared_dir
        pass
