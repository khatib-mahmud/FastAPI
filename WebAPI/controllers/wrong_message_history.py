from flask import jsonify
from flask.views import MethodView


class WrongMsgHistory(MethodView):

    def get(self, no_of_days):
        try:
            from Service.preprocess import PreProcess
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            print('get-wrong-msg-history api has been hit')
            from_date, to_date = PreProcess.calculate_date_range(no_of_days)
            chat_history = PreProcess.get_chat_history_list(
                all_chat_history=chat_response_db_obj.read_all_date_range(from_date, to_date))
            unanswered_or_wrong_msg_list = PreProcess.calculate_wrong_or_unanswered_msgs(chat_history)
            response = jsonify(unanswered_or_wrong_msg_list)
            return response

        except Exception as e:
            print(e)
            return str(e)
