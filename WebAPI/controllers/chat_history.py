from flask import jsonify
from flask.views import MethodView


class ChatHistory(MethodView):

    def get(self, no_of_days):
        try:
            from Service.preprocess import PreProcess
            chat_response_db_obj = PreProcess.get_chat_db_obj()
            print('ChatHistory api has been hit')
            from_date, to_date = PreProcess.calculate_date_range(no_of_days)
            chat_history_list = PreProcess.get_chat_history_list(chat_response_db_obj.read_all_from_date(from_date))

            # chat_history_list = []
            # for single_row_chat_history in all_chat_history:
            #     if single_row_chat_history.question is None:
            #         continue
            #     else:
            #         chat_history_list.append({
            #             'date_value': single_row_chat_history.date_value.strftime("%d/%m/%Y"),
            #             'time_value': single_row_chat_history.date_value.strftime("%H:%M"),
            #             'mobile_number': single_row_chat_history.mobile_number,
            #             'question': single_row_chat_history.question,
            #             'response': single_row_chat_history.response,
            #             'integrated_platform': single_row_chat_history.integrated_platform
            #         })

            return jsonify(chat_history_list)

        except Exception as e:
            print(e)
            return str(e)

# def get(self, no_of_days):
#     try:
#         chat_history_list, question_list, reply_list = [], [], []
#         date_value = any
#         from python_file.model.chat_response_db import ChatResponseDB
#         print('ChatHistory api has been hit')
#         from_date, to_date = PreProcess.calculate_date_range(no_of_days)
#         chat_history = PreProcess.get_chat_history_list(
#             all_chat_history=ChatResponseDB.read_all_date_range(from_date, to_date))
#         users_list = PreProcess.calculate_unique_items(
#             chat_history_list=chat_history, item_identifying_column_name='mobile_number')
#
#         for user in users_list:
#             chat_history_per_user = PreProcess.get_chat_history_list(ChatResponseDB.read_all_specific_user(user))
#             message_count = PreProcess.calculate_total_no_of_questions(chat_history_per_user)
#             for item in chat_history_per_user:
#                 question_list.append(item['question'])
#                 reply_list.append(item['response'])
#                 date_value = item['date_value']
#             chat_history_list.append({"date": date_value, "user_no": user, "message_count": message_count,
#                                       "question": question_list, "response": reply_list})
#             question_list = []
#             reply_list = []
#         return jsonify(chat_history_list)
#
#     except Exception as e:
#         print(e)
#         return str(e)
