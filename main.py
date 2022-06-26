from fastapi import FastAPI

import uvicorn

from controllers.items_controller import ItemController
from database import Base, engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware


async_mode = None
app = FastAPI()
app.debug = True

Base.metadata.create_all(engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_api_route('/item', endpoint=ItemController().get_item, methods=['GET'])
app.add_api_route('/item/{id}', endpoint=ItemController().get_single_item, methods=['GET'])
app.add_api_route('/add_item', endpoint=ItemController().add_item, methods=['POST'])
app.add_api_route('/update_item/{id}', endpoint=ItemController().update_item, methods=['PUT'])
app.add_api_route('/item-delete/{id}', endpoint=ItemController().delete_item, methods=['DELETE'])


if __name__ == "__main__":
    uvicorn.run(app, host="10.11.201.41", port=5003)
