
import firebase_admin
from typing import Optional
from google.cloud.firestore_v1 import Client
from firebase_admin import firestore, auth
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError




db: Optional[Client] = None  # This will be set later
# /etc/firebase/service_account.json


def initialize_firebase():
    global db
    cred = firebase_admin.credentials.Certificate("app/core/service_account.json") 
    firebase_admin.initialize_app(cred) 
    db = firestore.client()


def fetch_hello_docs(limit: int = 10, timeout: float = 5.0):
    global db
    if db is None:
        initialize_firebase()
    try:
        query = db.collection("hello").limit(limit)

        # Prefer non-blocking get with timeout if supported by library version
        try:
            docs = query.get(timeout=timeout)
            data = [doc.to_dict() for doc in docs]
            print("[Firebase] hello collection documents:", data)
            return data
        except TypeError:
            # Older google-cloud-firestore may not support `timeout` on get()
            pass

        # Fallback: run stream() in a background thread and enforce timeout
        def _fetch():
            return [doc.to_dict() for doc in query.stream()]

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_fetch)
            data = future.result(timeout=timeout)
            print("[Firebase] hello collection documents:", data)
            return data

    except Exception as e:
        print("[Firebase] Failed to fetch 'hello' collection documents:", e)
        return []
    