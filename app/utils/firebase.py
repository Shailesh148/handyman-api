
import firebase_admin
from typing import Optional
from google.cloud.firestore_v1 import Client
from firebase_admin import firestore, auth




db: Optional[Client] = None  # This will be set later



def initialize_firebase():
    global db
    cred = firebase_admin.credentials.Certificate("app/core/service_account.json") 
    firebase_admin.initialize_app(cred) 
    db = firestore.client()
    