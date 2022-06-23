# from server import app
# import os
# from pathlib import Path
# from urllib.parse import quote
# from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy
#
#
# dir_path = str(Path(__file__).parent.parent.parent)
# load_dotenv(dir_path + "/.env")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
#     user=os.getenv('user'), password=quote(os.getenv('password')), server=os.getenv('server'),
#     database=os.getenv('database'), pool_size=198, max_overflow=9)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
# db.init_app(app)
# engine_container = db.get_engine(app)
