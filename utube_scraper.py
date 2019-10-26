#! python 3
# This will save all video titles from a Youtube to a text file.

import os
import yaml
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    api_service_name = "youtube"
    api_version = "v3"
    #client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Ask for channel name ,test
    req_chnl = input("Which YouTube Channel do you want? ")
    print(req_chnl)


    #flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
       # client_secrets_file, scopes)
    #credentials = flow.run_console()
   # youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=cfg['api_key'])

    # Get ID based on channel name
    request = youtube.search().list(
        part="snippet",
        q=req_chnl
    )
    response = request.execute()
    print(response)

    # Get video upload list UUqmQ1b96-PNH4coqgHTuTlA
    # UUqmQ1b96-PNH4coqgHTuTlA tested
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId="UUbxb2fqe9oNgglAoYqsYOtQ"
    )
    upload_list = request.execute()
    print(upload_list)

    # List titles in file


if __name__ == "__main__":
    main()