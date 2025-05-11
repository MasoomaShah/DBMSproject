import firebase_admin
from firebase_admin import credentials, firestore

# Path to your JSON key
cred = credentials.Certificate("website/firebase/firebase-adminsdk.json")

# Initialize the app only once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

def add_user(email, password_hash):
    db.collection('Users').document(email).set({
        'email': email,
        'password': password_hash
    })
def verify_login(email, password_input):
    users_ref = db.collection('Users')
    query = users_ref.where('email', '==', email).limit(1).stream()

    for doc in query:
        data = doc.to_dict()
        return data['password'] == password_input  # simple match

    return False  # No matching email found

print(verify_login('tim@gmail.com','1234567'))