from flask import jsonify
from flask.views import MethodView


class DashboardAPI(MethodView):

    def get (self):
        try:
            print('get-dashboard-data api has been hit')
            from Scheduler.update_dashboardDB import UpdateDashboardDB
            from Service.preprocess import PreProcess
            dashboard_db_obj = PreProcess.get_dashboard_db_obj()
            UpdateDashboardDB.update_db()
            all_dashboard_info = dashboard_db_obj.read_all()
            dashboard_info_list = []
            for dashboard_info in all_dashboard_info:
                dashboard_info_list.append({
                    'total_no_of_users': dashboard_info.no_of_users,
                    'total_no_of_questions': dashboard_info.total_no_of_questions,
                    'integrated_platform': dashboard_info.integrated_platform
                })
            return jsonify({'all_dashboard_info': dashboard_info_list})

        except Exception as e:
            return e

    def post(self):
        return {"message": "post method api is called successfully"}
