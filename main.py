from fastapi import FastAPI
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool
import grpc._cython.cygrpc
import os
from urllib.parse import quote
from dotenv import load_dotenv
import uvicorn
from WebAPI.controllers.home import Home



async_mode = None
app = FastAPI()
app.debug = True
# dir_path = os.path.dirname(os.path.realpath(__file__))
# cred_path = dir_path + '/config/ava-existing-customer-v2.json'
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path



# @app.get('/')
# async def root():
#     return {"message": "Hello World"}

@app.get('/item/{id}')
async def read_item(id):
    return {"item-id": id}



app.add_api_route('/', endpoint= Home().get, methods=['GET'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5003)
