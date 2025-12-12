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
import requests
import os
def send_whatsapp_message(phone_number: str, name: str, url: str):
	"""
	Send a WhatsApp message using Facebook Graph API
	
	Args:
		phone_number: Recipient phone number (e.g., "918978938067")
		name: Name to include in the message template
		url: URL to include in the message template
	"""
	url_api = "https://graph.facebook.com/v22.0/876284132243072/messages"
	headers = {
		"Authorization": "Bearer " + os.getenv("WHATSAPP_API_AUTH_TOKEN", ""),
		"Content-Type": "application/json"
	}
	
	payload = {
		"messaging_product": "whatsapp",
		"to": phone_number,
		"type": "template",
		"template": {
			"name": "ticket_order",
			"language": {
				"code": "en_US"
			},
			"components": [
				{
					"type": "body",
					"sub_type": "",
					"index": 0,
					"parameters": [
						{
							"type": "text",
							"text": name
						},
						{
							"type": "text",
							"text": url
						}
					]
				}
			]
		}
	}
	
	try:
		response = requests.post(url_api, headers=headers, json=payload)
		response.raise_for_status()
		print(f"Successfully sent WhatsApp message to {phone_number}: {response.json()}")
		return response.json()
	except requests.exceptions.RequestException as e:
		print(f"Error sending WhatsApp message: {e}")
		if hasattr(e, 'response') and e.response is not None:
			print(f"Response: {e.response.text}")
		raise

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
		send_whatsapp_message(each_user_data.phone, event, "101inc-frontend.vercel.app/")
  
  
  
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