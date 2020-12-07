import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./firstdatabase-19295-firebase-adminsdk-c7g6z-c758718277.json')
app = firebase_admin.initialize_app(cred)

db = firestore.client()




users_ref = db.collection(u'users')
docs = users_ref.stream()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))