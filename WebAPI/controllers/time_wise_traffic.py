from flask import jsonify
from flask.views import MethodView


class TimeWiseTraffic(MethodView):

    def get(self, no_of_days):

        try:
            print('TimeWiseTraffic api has been hit')
            from Service.preprocess import PreProcess
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            from_date, to_date = PreProcess.calculate_date_range(no_of_days)
            specific_date_range_chat_history = chat_response_db_obj.read_all_date_range(from_date, to_date)
            specific_date_range_chat_history_list = PreProcess.get_chat_history_list(
                specific_date_range_chat_history)
            time_wise_traffic_list = PreProcess.calculate_time_from_date(specific_date_range_chat_history_list)
            return jsonify(time_wise_traffic_list)

        except Exception as e:
            print(e)
            return str(e)
