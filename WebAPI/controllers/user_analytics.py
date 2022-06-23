from flask import jsonify
from flask.views import MethodView


class UserAnalytics(MethodView):

    def get(self, no_of_days):
        try:
            try:
                from Service.preprocess import PreProcess
                chat_response_db_obj = PreProcess.get_chat_db_obj()
                user_analytics_list = []
                all_chat_history = chat_response_db_obj.read_all()
                from_date, to_date = PreProcess.calculate_date_range(no_of_days)
                new_user_chat_history = chat_response_db_obj.read_all_date_range(from_date, to_date)
                first_date = chat_response_db_obj.read_by_id(3).date_value
                total_user_chat_history = chat_response_db_obj.read_all_date_range(first_date, from_date)
                total_users_list = PreProcess.calculate_unique_items(PreProcess.get_chat_history_list(
                    total_user_chat_history), 'mobile_number')
                total_new_users_list = PreProcess.calculate_unique_items(PreProcess.get_chat_history_list(
                    new_user_chat_history), 'mobile_number')
                # if len(total_new_users_list) > len(total_users_list):
                #     return "Please Reduce Time Duration"
                new_users_percentage, returning_users_percentage, engaged_user_percentage = PreProcess.calculate_different_users(
                    PreProcess.get_chat_history_list(all_chat_history), total_users_list, total_new_users_list)
                user_analytics_list.append({
                    'new_users_percentage': new_users_percentage,
                    'returning_users_percentage': returning_users_percentage,
                    'engaged_users_percentage': engaged_user_percentage
                })

                response = jsonify(user_analytics_list)

                print('ServicesHitCount api has been hit')
            except Exception as e:
                print(e)
                return str(e)

            return response

        except Exception as e:
            return str(e)


class SpecificDateHistory(MethodView):

    def get(self, from_date, to_date):
        try:
            from Service.preprocess import PreProcess
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            specific_chat_history = chat_response_db_obj.read_all_date_range(from_date, to_date)
            specific_chat_history_list = PreProcess.get_chat_history_list(specific_chat_history)
            response = jsonify(specific_chat_history_list)
            print('get-specific-date-chat-history api has been hit')

            return response

        except Exception as e:
            return str(e)


class ChartDataByDateRange(MethodView):

    def get(self, from_date, to_date):
        try:
            from Service.preprocess import PreProcess
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            chart_data_list = []
            chart_history = chat_response_db_obj.read_all_date_range(from_date, to_date)
            chart_data = PreProcess.get_chat_history_list(chart_history)
            no_of_users = len(PreProcess.calculate_unique_items(chart_data, 'mobile_number'))
            wrong_answers_list = PreProcess.calculate_wrong_or_unanswered_msgs(chart_data)
            no_of_wrong_answers = len(PreProcess.calculate_unique_items(wrong_answers_list,
                                                                        'wrong_or_unanswered_msg_count'))
            no_of_right_answers = PreProcess.calculate_total_no_of_questions(chart_data) - no_of_wrong_answers
            chart_data_list.append({
                'no_of_users': no_of_users,
                'right_answers': no_of_right_answers,
                'wrong_answers': no_of_wrong_answers
            })
            response = jsonify(chart_data_list)

            print('ChartDataByDateRange api has been hit')

            return response

        except Exception as e:
            return str(e)
