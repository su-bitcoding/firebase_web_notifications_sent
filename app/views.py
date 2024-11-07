import requests
import json

from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from google.oauth2 import service_account
from google.auth.transport.requests import Request


def firebase_view(request):
    return render(request, "firebase_templates.html")


def showFirebaseJS(request):
    data = (
        'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");'
        'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); '
        "var firebaseConfig = {"
        # your create a web app in shoe the the api key
        '        apiKey: "",'
        # your web app authDomain
        '        authDomain: "",'
        # your web app project id
        '        projectId: "",'
        # your web app storage bucket
        '        storageBucket: "",'
        # your web app messaging sender id
        '        messagingSenderId: "",'
        # your web app app id
        '        appId: "",'
        # your web app measurement id
        '        measurementId: ""'
        " };"
        "firebase.initializeApp(firebaseConfig);"
        # when which type a show a notifications in a page
        "const messaging=firebase.messaging();"
        "messaging.setBackgroundMessageHandler(function (payload) {"
        "    console.log(payload);"
        "    const notification=JSON.parse(payload);"
        "    const notificationOption={"
        "        body:notification.body,"
        "        icon:notification.icon"
        "    };"
        "    return self.registration.showNotification(payload.notification.title,notificationOption);"
        "});"
    )

    return HttpResponse(data, content_type="text/javascript")


# this is a function to get the token and that token is pass in header to used to send a notification
# this token is expire after 1 hour
def generate_auth_token():
    """Generate auth token"""

    # You can download this file from the Firebase console in project settings in Service Accounts in the Generate new private key section
    # Path to your service account key file
    KEY_FILE_PATH = "/home/pc/Desktop/firebase_web_notifications_sent/firebase_key.json"

    # Define the required scope for FCM
    SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

    # Load the credentials from the service account file
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE_PATH, scopes=SCOPES
    )

    # Request a new token
    credentials.refresh(Request())

    return credentials.token


# this is a function to send a notification
def push_notification(token, title, body, bearer_token):
    """Send push message"""

    url = f"https://fcm.googleapis.com/v1/projects/testing1-bb5a2/messages:send"
    payload = json.dumps(
        {
            "message": {
                "token": token,  # the token is generate a token is frontend side
                "webpush": {
                    "notification": {
                        "title": title,  # title of the notification
                        "body": body,  # body of the notification
                        "icon": "https://classdekho.com/static/images1/logo.png",  # your icon
                    },
                    "fcmOptions": {
                        "link": "http://127.0.0.1:8001/",  # your link when through a generate a token that is click enable in the notification
                    },
                },
            }
        }
    )
    headers = {
        "Authorization": f"Bearer {bearer_token}",  # bearer token is generate a token is generate_auth_token function
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)


# this is a function to send a notification
class SentNotificationView(APIView):
    def post(self, request):
        auth_token = generate_auth_token()

        token = request.data.get("token")
        title = request.data.get("title")
        body = request.data.get("body")

        if not token or not title or not body:
            return Response(
                {"error": "Token, title, and body are required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            push_notification(token, title, body, auth_token)
            return Response(
                {"message": "Notification sent successfully!"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"Error sending notification: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
