#! python 3
# This will save all video titles from a Youtube to a text file.

import os
import yaml
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    channels = []
    videos = []

    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    api_service_name = "youtube"
    api_version = "v3"
    #client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Ask for channel name ,test
    req_chnl = input("Which YouTube Channel do you want? ")


    #flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
       # client_secrets_file, scopes)
    #credentials = flow.run_console()
   # youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=cfg['api_key'])

    # Get ID based on channel name
    search_response = youtube.search().list(
        part="snippet",
        q=req_chnl
    ).execute()

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                       search_result['id']['videoId']))
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s (%s)' % (search_result['snippet']['title'],
                                         search_result['id']['channelId']))
    # print("JSON Respone: " + search_response)
    print('Channels Found:\n', '\n'.join(channels), '\n')

    print('Videos:\n', '\n'.join(videos), '\n')



    # Get video upload list UUqmQ1b96-PNH4coqgHTuTlA
    # UUqmQ1b96-PNH4coqgHTuTlA tested
    video_response = youtube.playlistItems().list(
        part="snippet",
        playlistId="UUbxb2fqe9oNgglAoYqsYOtQ"
    ).execute()

    #print("JSON Response: " + video_json)

    # List titles in file


if __name__ == "__main__":
    main()