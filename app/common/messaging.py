from app.schemas.messaging import NotificationQuery
from firebase_admin import messaging
from app.utils.firebase import db
from sqlalchemy.orm import Session
from app.models.user import AppUser
from app.models.user_device import UserDevice
from app.models.ticket import Ticket
from app.core.db import get_db
from app.core.db import SessionLocal
from fastapi import APIRouter, status, Depends

def send_notification(user_role: str, event: str, ticket_id: str = None):
	db = SessionLocal()
	notification_query = events_list_data.get(event)
	user_data = []
	if user_role == "OPERATOR":
		user_data = db.query(AppUser).filter(AppUser.role == "OPERATOR").all()
	else:
		ticket_data = db.query(Ticket).filter(Ticket.id == ticket_id).first()

		user_data = db.query(AppUser).filter(AppUser.id == ticket_data.customer_id).all() 

	for each_user_data in user_data:
		print(each_user_data.id)
		user_devices = db.query(UserDevice).filter(UserDevice.user_id == each_user_data.id).all()

		for each_user_device in user_devices:
			message = messaging.Message(
				token=each_user_device.fcm_token,
				notification=messaging.Notification(
					title=notification_query.get("title", ""),
					body=notification_query.get("body", "")
				),
				data = {
    				"url": "https://101inc-frontend.vercel.app/"
  				}
			)
			try:
				response = messaging.send(message)
				print("Successfully sent message:", response)
			except Exception as e:
				print("Error sending message:", e)
  
  
  
events_list_data = {
	"ticket_created":{
		"title": "Ticket Created",
  		"body": "Customer has created a new ticket."
	},
 	"ticket_estimated": {
		"title": "Estimation Provided",
  		"body": "An estimation has been provided for your ticket."
	},
   	"estimate_accepted": {
		"title": "Estimation Accepted",
  		"body": "Estimate has been accepted by the user"
	},
    "estimate_rejected": {
		"title": "Estimation Rejected",
  		"body": "Estimate has been rejected by the user"
	},
    "ticket_completed": {
		"title": "Repair Task Completed",
        "body": "Repiar task been completed. Thank you for using our service"
	} 
}