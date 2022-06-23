from flask import jsonify
from flask.views import MethodView


class SpecificUserHistory(MethodView):

    def get(self, mobile_number):
        try:
            print('get-specific-user-chat-history api has been hit')
            from Service.preprocess import PreProcess
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            user_mobile_number = mobile_number
            specific_user_chat_history_list = PreProcess.get_chat_history_list(
                chat_response_db_obj.read_all_specific_user(user_mobile_number))
            response = jsonify(specific_user_chat_history_list)
            return response

        except Exception as e:
            return str(e)