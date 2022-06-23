from flask import jsonify
from flask.views import MethodView

BTN_LIST = ['A/C OPENING', 'EKYC', 'PRODUCTS', 'SHADHIN CARD', 'FEES',
            'LOAN', 'CREDIT CARD', 'DEBIT CARD', 'AGENT BANKING']


class BotLeadReport(MethodView):

    def get(self, no_of_days):
        try:
            from Service.preprocess import PreProcess
            # preprocess_obj = GetServiceObject.get_preprocess_object()
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            print('BotLeadReport api has been hit')
            leads = []
            from_date, to_date = PreProcess.calculate_date_range(no_of_days)
            chat_history_list = PreProcess.get_chat_history_list(chat_response_db_obj.read_all_from_date(from_date))

            for item in chat_history_list:
                question = item['question'].upper()
                for btn in BTN_LIST:
                    if btn in question:
                        leads.append(item)

            return jsonify(leads)

        except Exception as e:
            print(e)
            return str(e)
