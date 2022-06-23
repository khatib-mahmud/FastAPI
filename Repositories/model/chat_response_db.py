from server import db, engine_container

from sqlalchemy import func


class ChatResponseDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_value = db.Column(db.DateTime(90))
    mobile_number = db.Column(db.String(90))
    question = db.Column(db.TEXT(9000))
    response = db.Column(db.TEXT(9000))
    integrated_platform = db.Column(db.String(90))

    def __init__(self, date_value=None, mobile_number=None, question=None, response=None):
        db.create_all()
        self.date_value = date_value
        self.mobile_number = mobile_number
        self.question = question
        self.response = response
        self.integrated_platform = 'Web'

    @staticmethod
    def add_data(date_value=None, mobile_number=None, question=None, response=None):
        chat_log = ChatResponseDB(date_value, mobile_number, question, response)
        db.session.add(chat_log)
        db.session.commit()
        db.session.close()
        db.session.remove()
        db.engine.dispose()
        engine_container.dispose()

    @staticmethod
    def update_data(filter_by_mobile_number_value, update_value):
        update_this = ChatResponseDB.query.filter_by(mobile_number=filter_by_mobile_number_value).first()
        update_this.mobile_number = update_value
        db.session.commit()
        db.session.close()
        db.session.remove()
        db.engine.dispose()
        engine_container.dispose()

    @staticmethod
    def read_all_specific_user(mobile_number):
        specific_user_data = ChatResponseDB.query.filter_by(mobile_number=mobile_number).all()
        return specific_user_data

    @staticmethod
    def read_all_specific_date(date):
        specific_user_data = ChatResponseDB.query.filter_by(date_value=date).all()
        return specific_user_data

    @staticmethod
    def read_all_date_range(from_date, to_date):
        specific_user_data = db.session.query(ChatResponseDB).filter(ChatResponseDB.date_value >= from_date,
                                                                     ChatResponseDB.date_value <= to_date).all()
        return specific_user_data

    @staticmethod
    def read_all_from_date(from_date):
        specific_user_data = db.session.query(ChatResponseDB).filter(ChatResponseDB.date_value >= from_date).order_by(
            ChatResponseDB.date_value.desc()).all()
        return specific_user_data

    @staticmethod
    def read_date_by_user(user):
        specific_user_data = db.session.query(ChatResponseDB).filter(
            ChatResponseDB.mobile_number == user).first()

        return specific_user_data

    @staticmethod
    def read_by_id(id):
        chat_history_by_id = ChatResponseDB.query.filter_by(id=id).first()
        return chat_history_by_id

    @staticmethod
    def max():
        max_value = db.session.query(func.max(ChatResponseDB.id)).scalar()
        return max_value

    @staticmethod
    def read_all():
        all_data = ChatResponseDB.query.all()
        return all_data

    @staticmethod
    def delete_data(value):
        delete_this = ChatResponseDB.query.filter_by(mobile_number=value).first()
        db.session.delete(delete_this)
        db.session.commit()
        db.session.close()
        db.engine.dispose()
        engine_container.dispose()

# if __name__ == '__main__':
#
#     print("Success")
