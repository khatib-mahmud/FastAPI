import http.client
import json

from flask import request
from flask.views import MethodView


class AuthController(MethodView):
    def __init__(self):
        self.__base_url: str = '10.88.1.88'
        self.__port: int = 82
        self.__log_in_route: str = '/api/User/LogIn'

    def post(self):
        try:
            client_object = http.client.HTTPConnection(self.__base_url, self.__port, timeout=999)
            user_credentials = request.get_json(force=True)
            payload = json.dumps(user_credentials)
            client_object.request(method='POST',
                                  url=self.__log_in_route,
                                  body=payload,
                                  headers={'Content-type': 'application/json'})
            response = client_object.getresponse()
            response = response.read().decode()
            client_object.close()
            return response
        except Exception as e:
            print(str(e))
            return {"apiData": None, "message": str(e), "isExecute": False, "totalRecord": 0}
