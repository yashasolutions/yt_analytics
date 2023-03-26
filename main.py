import json
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "client_secrets_oauth.json"
api_service_name = "youtube"
api_version = "v3"


def get_google_api_credentials():

    try:
        with open(CLIENT_SECRETS_FILE) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("File not found")
        exit()

    else:
        client_id = data['installed']['client_id']
        client_secret = data['installed']['client_secret']

        scopes = ["https://www.googleapis.com/auth/yt-analytics.readonly", "https://www.googleapis.com/auth/youtube.readonly"]

        try:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, scopes=scopes)

        except ValueError:
            print("Invalid client secrets file")
            exit()
        else:
            flow.run_local_server( host='localhost',
                                port=8080,
                                authorization_prompt_message='Please visit this URL: {url}',
                                success_message='The auth flow is complete; you may close this window.',
                                open_browser=True)
            credentials = flow.credentials
            return credentials

def get_youtube_channel_data(credentials):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()
    return response

def main():
    global credentials
    credentials = get_google_api_credentials()
    print(credentials.token)
    print(credentials.refresh_token)
    print(credentials.expiry)

    # response = get_youtube_channel_data(credentials)
    # print(response)

if __name__ == "__main__":
    main()
