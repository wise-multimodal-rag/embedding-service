from starlette import status

from app.config import settings
from app.src.exception.service import SampleServiceError


def load_mock_items():
    # mock data
    fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}
    return fake_items_db


def read_item_from_db(item_id):
    fake_items_db = load_mock_items()
    if item_id not in fake_items_db.keys():
        raise SampleServiceError(
            code=int(str(settings.SERVICE_CODE) + str(status.HTTP_404_NOT_FOUND)),
            message="Item not found", result={}
        )
    return fake_items_db[item_id]["name"]


def update_item_to_db(item_id):
    if item_id != "plumbus":
        raise SampleServiceError(
            code=int(str(settings.SERVICE_CODE) + str(status.HTTP_403_FORBIDDEN)),
            message="You can only update the item: plumbus", result={}
        )
    return "The great Plumbus"
