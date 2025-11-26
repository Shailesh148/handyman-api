from firebase_admin import messaging

from fastapi import APIRouter, status, Depends
from app.schemas.messaging import NotificationQuery
from app.utils.firebase import fetch_hello_docs

router =APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def send_push_notification(notification_query: NotificationQuery):
    message = messaging.Message(
        token=notification_query.token,
        notification=messaging.Notification(
            title=notification_query.title,
            body=notification_query.body
        ),
        # data=notification_query.body or {}
    )
    # data = fetch_hello_docs()
    try:
        response = messaging.send(message)
        print("Successfully sent message:", response)
    except Exception as e:
        print("Error sending message:", e)
    return "data"