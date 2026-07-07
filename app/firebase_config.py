import firebase_admin

from firebase_admin import credentials

cred = credentials.Certificate(
    "app/harvester-app-59192-firebase-adminsdk-fbsvc-509feeee7a.json"
)

firebase_admin.initialize_app(cred)