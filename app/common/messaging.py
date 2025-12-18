from app.schemas.messaging import NotificationQuery
from firebase_admin import messaging
from app.utils.firebase import db
from sqlalchemy.orm import Session
from app.models.user import AppUser
from app.models.user_device import UserDevice
from app.models.ticket import Ticket
from app.models.inventory import Inventory
from app.models.garage import Garage
from app.core.db import get_db
from app.core.db import SessionLocal
from fastapi import APIRouter, status, Depends
import requests
import os
def send_whatsapp_message(phone_number: str, template_name: str, *template_params: str):
	"""
	Send a WhatsApp message using Facebook Graph API
	
	Args:
		phone_number: Recipient phone number (e.g., "918978938067")
		template_name: WhatsApp template name
		template_params: Variable number of body text parameters
	"""
	url_api = "https://graph.facebook.com/v22.0/876284132243072/messages"
	headers = {
		"Authorization": "Bearer " + os.getenv("WHATSAPP_API_AUTH_TOKEN", ""),
		"Content-Type": "application/json"
	}
	
	# Build template parameters dynamically, skipping None values
	parameters = [{"type": "text", "text": str(p)} for p in template_params if p is not None]
	
	body_component = {
		"type": "body",
		"sub_type": "",
		"index": 0
	}
	if parameters:
		body_component["parameters"] = parameters
	
	payload = {
		"messaging_product": "whatsapp",
		"to": phone_number,
		"type": "template",
		"template": {
			"name": template_name,
			"language": {
				"code": "en_US"
			},
			"components": [body_component]
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

def send_notification(user_role: str, event: str, url: str = None, ticket_id: str = None):
	db = SessionLocal()
	notification_query = events_list_data.get(event)
	user_data = []
	if user_role == "OPERATOR":
		user_data = db.query(AppUser).filter(AppUser.role == "OPERATOR").all()
	else:
		ticket_data = db.query(Ticket).filter(Ticket.id == ticket_id).first()

		user_data = db.query(AppUser).filter(AppUser.id == ticket_data.customer_id).all() 

	for each_user_data in user_data:
		template_params = [event]
		if url is not None:
			template_params.append(url)
		send_whatsapp_message(each_user_data.phone, "ticket_status", *template_params)
  

def send_admin_reorder_notification(user_role: str, event: str, inv: Inventory):
	db = SessionLocal()
	# notification_query = events_list_data.get(event)
	garage_data = []
	
	garage_data = db.query(Garage).filter(Garage.id == inv.garage_id).first()
	
	template_params = [
		garage_data.name,
		inv.item.name,
		f"https://101inc-frontend.vercel.app/en/admin/garage-management/{inv.garage_id}",
	]
	send_whatsapp_message("+9779840136833", "inventory_reorder_improved", *template_params)
  
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