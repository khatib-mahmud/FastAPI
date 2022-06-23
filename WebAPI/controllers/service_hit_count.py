from flask import jsonify
from flask.views import MethodView


class ServicesHitCount(MethodView):

    def get(self, no_of_days):
        try:
            print('ServicesHitCount api has been hit')
            from Service.preprocess import PreProcess
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            from_date, to_date = PreProcess.calculate_date_range(no_of_days)
            specific_date_chat_history = chat_response_db_obj.read_all_date_range(from_date, to_date)
            services_hit_count_list = PreProcess.calculate_most_clicked_btn(PreProcess.get_chat_history_list(
                specific_date_chat_history))

            response = jsonify(services_hit_count_list)
            # total_user_list = PreProcess.calculate_different_users(PreProcess.get_chat_history_list(all_chat_history))
            # print(total_user_list)
            return response

        except Exception as e:
            return str(e)
