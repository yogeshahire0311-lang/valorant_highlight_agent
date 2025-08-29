import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

class YouTubeUploader:
    def __init__(self, config):
        self.client_secret = config["upload"]["client_secret"]
        self.privacy = config["upload"].get("privacy", "unlisted")
        self.service = self.authenticate()

    def authenticate(self):
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]

        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                self.client_secret, scopes)
            creds = flow.run_local_server(port=0)
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    def upload(self, filepath, title="Valorant Highlight", description="Highlight clip"):
        request = self.service.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": ["valorant", "highlight", "gaming", "fps", "esports"],
                    "categoryId": "20"
                },
                "status": {
                    "privacyStatus": self.privacy
                }
            },
            media_body=googleapiclient.http.MediaFileUpload(filepath)
        )
        response = request.execute()
        return f"https://youtu.be/{response['id']}"
