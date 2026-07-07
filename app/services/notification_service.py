from firebase_admin import messaging
from app.models.notification import Notification

def create_notification(
    db,
    user_id,
    title,
    message
):
    print("Saving notification into DB...")
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message
    )

    db.add(notification)
    db.commit()
    print("Notification saved.")

def send_notification(
    token,
    title,
    body
):
    print("==========")
    print("TOKEN:", token)
    print("TITLE:", title)
    print("BODY:", body)

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )

    response = messaging.send(message)

    print("FCM RESPONSE:", response)
    print("==========")