from firebase_admin import messaging
from app.schemas.messaging import NotificationQuery
from app.utils.firebase import fetch_hello_docs


def send_push_notification(payload: NotificationQuery):
    message = messaging.Message(
        token=payload.token,
        notification=messaging.Notification(
            title=payload.title,
            body=payload.body,
        ),
    )
    data = fetch_hello_docs()
    response = messaging.send(message)
    return data


