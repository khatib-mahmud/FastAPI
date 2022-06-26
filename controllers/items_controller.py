from model.items import Item
from entities.item_model import ItemModel

from fastapi import Body, Depends

from sqlalchemy.orm import Session

from database import SessionLocal


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class ItemController:
    def __init__(self):
        pass

    def get_item(self,session: Session = Depends(get_session)):
        print("Get item api hit")
        items = session.query(ItemModel).all()

        body = {
            "responsecode": 200,
            "data": items
        }
        return body

    def get_single_item(self, id:int, session: Session = Depends(get_session)):
        print("Get single item api  hit")

        allitemLen = session.query(ItemModel).all()
        if 0 < id <= len(allitemLen):

            item = session.query(ItemModel).get(id)

            body = {
                "responsecode": 200,
                "data": item

            }
            return body
        else:
            body = {
                "responsecode": 402,
                "data": "This is not a valid id."

            }
            return body


    def add_item(self, item: Item, session: Session = Depends(get_session)):
        print("add item api hit")
        item = ItemModel(task=item.task)
        session.add(item)
        session.commit()
        session.refresh(item)

        body= {
            "responsecode": 200,
            "data": item
        }
        return body

    def update_item(self, id:int,item: Item, session: Session = Depends(get_session)):
        print("update item api hit")
        allitemLen = session.query(ItemModel).all()
        if 0 < id <= len(allitemLen):
            itemObj = session.query(ItemModel).get(id)
            itemObj.task = item.task

            session.commit()

            body= {
                "responsecode": 200,
                "data": item
            }
            return body
        else:
            body = {
                "responsecode": 402,
                "data": "This is not a valid id."

            }
            return body

    def delete_item(self,id:int, item: Item, session: Session = Depends(get_session)):
        print("delete item api hit")
        itemObject = session.query(ItemModel).get(id)
        session.delete(itemObject)
        session.commit()
        session.close()
        allItem = session.query(ItemModel).all()

        body = {
            "responsecode": 200,
            "data": allItem
        }
        return body

