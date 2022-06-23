from server import db, engine_container


class DashboardInfoDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_of_users = db.Column(db.String(90))
    total_no_of_questions = db.Column(db.String(90))
    integrated_platform = db.Column(db.String(90))

    def __init__(self, no_of_users=None, total_no_of_questions=None, integrated_platform=None):
        db.create_all()
        self.no_of_users = no_of_users
        self.total_no_of_questions = total_no_of_questions
        self.integrated_platform = integrated_platform

    @staticmethod
    def add_data(no_of_users=None, total_no_of_questions=None, integrated_platform=None):
        dash_info = DashboardInfoDB(no_of_users, total_no_of_questions, integrated_platform)
        db.session.add(dash_info)
        db.session.commit()
        db.session.close()
        db.session.remove()
        db.engine.dispose()
        engine_container.dispose()

    @staticmethod
    def update_data(filter_by_id_value=None, updated_no_of_users=None, updated_total_no_of_question=None,
                    updated_integrated_platform=None):
        update_this = DashboardInfoDB.query.filter_by(id=filter_by_id_value).first()
        update_this.no_of_users = updated_no_of_users
        update_this.total_no_of_questions = updated_total_no_of_question
        update_this.integrated_platform = updated_integrated_platform
        db.session.commit()
        db.session.close()
        db.session.remove()
        db.engine.dispose()
        engine_container.dispose()

    @staticmethod
    def read_no_of_users(read_by_id_value):
        user_all_data = DashboardInfoDB.query.filter_by(id=read_by_id_value).first()
        return user_all_data

    @staticmethod
    def read_all():
        all_data = DashboardInfoDB.query.all()
        return all_data

    @staticmethod
    def delete_data(value):
        delete_this = DashboardInfoDB.query.filter_by(no_of_users=value).first()
        db.session.delete(delete_this)
        db.session.commit()
        db.session.close()
        db.session.remove()
        db.engine.dispose()
        engine_container.dispose()

# if __name__ == '__main__':
#
#     print("Success")
