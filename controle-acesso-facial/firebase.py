import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('firebase-secret.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'REPLACE WITH YOUR FIREBASE DATABASE URL'
})

ref = db.reference('access')
