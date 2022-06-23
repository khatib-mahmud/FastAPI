from flask import jsonify, request
from flask.views import MethodView
from datetime import datetime
i = 0


class DBLoadTest(MethodView):

    def get(self):

        try:
            global i
            i += 1
            print('DBLoadTest api has been hit')
            from Service.preprocess import PreProcess
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            intent_info = request.get_json(force=True)
            message = intent_info["message"]
            input_no = intent_info["input_no"]
            bot_response = intent_info["bot_response"]
            date_value = datetime.today()
            chat_response_db_obj.add_data(date_value, input_no, message, bot_response)
            print(i)
            return "success"

        except Exception as e:
            print(e)
            return str(e)
