from fastapi import APIRouter, status
from app.schemas.messaging import NotificationQuery
from app.services.messaging_service import send_push_notification as svc_send_push_notification
router =APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def send_push_notification(notification_query: NotificationQuery):
    try:
        data = svc_send_push_notification(notification_query)
        print("Successfully sent message")
    except Exception as e:
        print("Error sending message:", e)
    return data