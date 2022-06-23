from flask import jsonify
from flask.views import MethodView
ACCOUNT_OPENING = 'A/C OPENING INFORMATION'
LOAN = 'LOAN'


class PotentialClients(MethodView):

    def get(self, no_of_days):
        try:
            from Service.preprocess import PreProcess
            chat_response_db = PreProcess.get_chat_db_obj()
            print('PotentialClients api has been hit')
            potential_clients = []
            from_date, to_date = PreProcess.calculate_date_range(no_of_days)
            chat_history_list = PreProcess.get_chat_history_list(chat_response_db.read_all_from_date(from_date))

            for item in chat_history_list:
                question = item['question'].upper()
                if (ACCOUNT_OPENING in question) or (LOAN in question):
                    potential_clients.append(item)

            return jsonify(potential_clients)

        except Exception as e:
            print(e)
            return str(e)
