import firebase_admin
from firebase_admin import credentials, firestore

# Path to your JSON key
cred = credentials.Certificate("website/firebase/firebase-adminsdk.json")

# Initialize the app only once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

def add_user(email, password):
    db.collection('Users').document(1).set({
        'email': email,
        'password': password
    })
def verify_login(email, password_input):
    users_ref = db.collection('Users')
    query = users_ref.where('email', '==', email).limit(1).stream()

    for doc in query:
        data = doc.to_dict()
        print(f"Fetched data: {data}")  # DEBUG
        print(f"Input password: {password_input}")
        print(f"Stored password: {data['password']}")
        return data['password'] == password_input
    print("No user found for that email")
    return False


print(verify_login('qasim.riaz@giki.edu.pk','1234567'))  

 # should print a list of user docs or be empty
