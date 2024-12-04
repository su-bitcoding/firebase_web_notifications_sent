import requests
import json

from django.http import HttpResponse
from django.shortcuts import render
from google.oauth2 import service_account
from google.auth.transport.requests import Request


def show_notification(request):
    data = (
        'importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js");'
        'importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js");'
        "var firebaseConfig = {"
        '    apiKey: "",'
        '    authDomain: "",'
        '    projectId: "",'
        '    storageBucket: "",'
        '    messagingSenderId: "",'
        '    appId: "",'
        '    measurementId: ""'
        "};"
        "firebase.initializeApp(firebaseConfig);"
        "const messaging = firebase.messaging();"
        "messaging.setBackgroundMessageHandler(function(payload) {"
        '    const notificationTitle = payload.notification?.title || "No Title";'
        "    const notificationOptions = {"
        '        body: payload.notification?.body || "No Body",'
        '        icon: payload.notification?.icon || "https://via.placeholder.com/128"'
        "    };"
        "    return self.registration.showNotification(notificationTitle, notificationOptions);"
        "});"
    )
    return HttpResponse(data, content_type="text/javascript")


def generate_auth_token():
    """
    Generate an authentication token for Firebase Cloud Messaging.
    """
    print("********* Generating auth token *********")
    KEY_FILE_PATH = (
        "firebase_key.json"  # Update with your service account JSON file path
    )
    SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

    # Load credentials and refresh token
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE_PATH, scopes=SCOPES
    )
    credentials.refresh(Request())
    print("********* Auth token generated *********")
    return credentials.token


def push_notification(token, title, body, auth_token):
    """
    Send a push notification using Firebase Cloud Messaging.
    """
    print("********* Sending push notification *********")
    url = "https://fcm.googleapis.com/v1/projects/classdekho-ca375/messages:send" # Update with your project ID

    payload = json.dumps(
        {
            "message": {
                "token": token,
                "webpush": {
                    "notification": {
                        "title": title,
                        "body": body,
                        "icon": "https://classdekho.com/static/images1/logo.png",
                    },
                    "fcmOptions": {"link": "http://127.0.0.1:8000/"},
                },
            }
        }
    )

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        print("********* Sending push notification *********")
    else:
        print("********* Failed to send notification *********", response.text)
        response.raise_for_status()


def notification_sender_view(request):
    """
    Renders the notification sender HTML form and handles form submissions.
    """
    if request.method == "POST":
        print("********* Processing notification sending form *********")
        token = request.POST.get("token")
        title = request.POST.get("title")
        body = request.POST.get("body")

        try:
            auth_token = generate_auth_token()
            push_notification(token, title, body, auth_token)
            print("********* Notification sent successfully *********")
        except Exception as e:
            print("********* Error sending notification *********", e)

    print("********* Rendering notification form *********")
    return render(request, "notifications.html")
