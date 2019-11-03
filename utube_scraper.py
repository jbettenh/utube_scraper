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
    uploads = []
    videos = []

    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    api_service_name = "youtube"
    api_version = "v3"
    #client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Ask for channel name ,test
    req_chnl = input("Which YouTube Channel do you want?\n")


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
        if search_result['id']['kind'] == 'youtube#channel':
           channels.append('%s (%s)' % (search_result['snippet']['title'],
                                     search_result['id']['channelId']))
           fnd_id=search_result['id']['channelId']
    print(search_response)
    print("\nChannels Found:\n", '\n'.join(channels), '\n')

    # Get Uploads ID
    uploads_response = youtube.channels().list(
        part="contentDetails",
        id=fnd_id
    ).execute()
    print("Uploads Response")
    print(uploads_response)

    for uploads_result in uploads_response.get('items', []):
        #if uploads_result['kind'] == 'youtube#channel':
         #  uploads.append('%s' % (uploads_result['contentDetails']['relatedPlaylists']['uploads']))
        uploads_id = uploads_result['contentDetails']['relatedPlaylists']['uploads']

    print("Uploads ID:")
    print(uploads_id)
    # Get video upload list
    video_response = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_id
    ).execute()

    for playlist_result in video_response.get('items', []):
        if playlist_result['kind'] == 'youtube#playlistItem':
            videos.append('%s' % (playlist_result['snippet']['title']))
            #videos.append('%s (%s)' % (playlist_result['snippet']['title'],
             #                          playlist_result['resourceId']['videoId']))

    print("Videos:\n", '\n'.join(videos), '\n')

    # List titles in file
    with open('video.txt', 'w') as file:
        # file.write(json.dumps(videos))
        json.dump(videos, file, indent=2)

if __name__ == "__main__":
    main()