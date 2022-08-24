import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

firestore_db = firestore.client()


docs = firestore_db.collection(u'Datos_Estudiantes').stream()

count = 0
documents = [snapshot.reference for snapshot in firestore_db.collection('Datos_Estudiantes').get()]
for document in documents:
    document.update({u'Huella': ''})
    count += 1
    print(document)
    print(count)

print(count)

'''
for doc in docs:
    data = {
        u'Huella': u''
    }

    doc.co.update(data)

    print(doc)
'''
