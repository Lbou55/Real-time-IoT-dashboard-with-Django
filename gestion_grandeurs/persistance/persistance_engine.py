from django.utils.dateparse import parse_datetime
from asgiref.sync import sync_to_async
import json
from django.apps import apps
import pyrebase
import firebase_admin
from firebase_admin import credentials

firebaseConfig = {
}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()

try:
    cred = credentials.Certificate("certificat_firebase.json")
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Firebase Admin failed to initialize: {e}")

@sync_to_async
def persist_to_firebase(message):
    message = json.loads(message)
    print(f"persisting to firebase: {message}")
    try:
        database.child("mesures").push(message)
    except Exception as e:
        print(f"error occured while persisting to firebase: {e}")

@sync_to_async
def persist_mesure(message):
    Grandeur = apps.get_model("grandeurs", "Grandeur")
    Mesure = apps.get_model("grandeurs", "Mesure")
    data = json.loads(message)

    grandeur = Grandeur.objects.get(nom="Temperature")
    print(f"persisting to DB: {data}")
    
    Mesure.objects.create(
        valeur=float(data["valeur"]),
        datePrise=parse_datetime(data["date_prise"]), # Check if your models.py uses datePrise or date_prise!
        grandeur=grandeur,
    )

buffer = []

@sync_to_async # <--- FIXED: Added missing decorator
def persiste_mesure_bulk(message):
    from grandeurs.models import Grandeur, Mesure
    data = json.loads(message)
    global buffer

    grandeur = Grandeur.objects.get(nom="Temperature")
    buffer.append(
        Mesure(
            valeur=float(data["valeur"]),
            datePrise=parse_datetime(data["date_prise"]), 
            grandeur=grandeur,
        )
    )
    
    if len(buffer) >= 1: # <--- FIXED: Changed 100 to 1 for instant saving
        Mesure.objects.bulk_create(buffer)
        print(f"Inserted {len(buffer)} rows into SQLite!")
        buffer.clear()
