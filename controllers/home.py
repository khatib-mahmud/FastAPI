# from flask.views import MethodView

class Home:
    def __init__(self):
        pass

    def get(self):
        return {"message": "Hello World"}
