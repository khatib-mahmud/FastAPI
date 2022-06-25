from fastapi import FastAPI

import uvicorn

from WebAPI.controllers.items_controller import ItemController
from database import Base, engine, SessionLocal

async_mode = None
app = FastAPI()
app.debug = True
Base.metadata.create_all(engine)


app.add_api_route('/item', endpoint=ItemController().get_item, methods=['GET'])
app.add_api_route('/item/{id}', endpoint=ItemController().get_single_item, methods=['GET'])
app.add_api_route('/add_item', endpoint=ItemController().add_item, methods=['POST'])
app.add_api_route('/update_item/{id}', endpoint=ItemController().update_item, methods=['PUT'])
app.add_api_route('/item-delete/{id}', endpoint=ItemController().delete_item, methods=['DELETE'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5003)
