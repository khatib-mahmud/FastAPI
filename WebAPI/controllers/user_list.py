from flask import jsonify
from flask.views import MethodView


class UserList(MethodView):

    def get(self, no_of_days):
        try:
            from Service.preprocess import PreProcess
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            print('UserList api has been hit')
            list_of_users = []
            from_date, to_date = PreProcess.calculate_date_range(no_of_days)
            users = chat_response_db_obj.read_all_date_range(from_date, to_date)
            users_list = PreProcess.calculate_unique_items(PreProcess.get_chat_history_list(users), 'mobile_number')

            for user in users_list:
                date_value = str(chat_response_db_obj.read_date_by_user(user).date_value)
                list_of_users.append({'mobile_number': user, 'date_of_user': date_value})

            response = jsonify(list_of_users)
            return response

        except Exception as e:
            print(e)
            return str(e)
