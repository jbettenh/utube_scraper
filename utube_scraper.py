#! python 3
# This will save all video titles from a Youtube to a text file.

import os
import yaml
import googleapiclient.discovery
import googleapiclient.errors
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
def get_service():


def get_channel_id():
    channels = []

    # Ask for channel name ,test
    req_chnl = input("Which YouTube Channel do you want?\n")

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
           return search_result['id']['channelId']
    print("\nChannels Found:\n", '\n'.join(channels), '\n')

    return None

def get_uploads_list(fnd_id):
    uploads = []
    # Get Uploads ID
    uploads_response = youtube.channels().list(
        part="contentDetails",
        id=fnd_id
    ).execute()

    for uploads_result in uploads_response.get('items', []):
        #if uploads_result['kind'] == 'youtube#channel':
         #  uploads.append('%s' % (uploads_result['contentDetails']['relatedPlaylists']['uploads']))
        return uploads_result['contentDetails']['relatedPlaylists']['uploads']

    return None

def get_video_list(uploads_id):
    videos = []

    # Get video upload list
    video_response = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_id,
        maxResults=50
    ).execute()

    for playlist_result in video_response.get('items', []):
        if playlist_result['kind'] == 'youtube#playlistItem':
            videos.append('%s' % (playlist_result['snippet']['title']))
            #videos.append('%s (%s)' % (playlist_result['snippet']['title'],
             #                          playlist_result['resourceId']['videoId']))

    print("Videos:\n", '\n'.join(videos), '\n')
    return None

def output_text(vid_txt):
    # List titles in file
    with open('video.txt', 'w') as file:
        # file.write(json.dumps(videos))
        json.dump(vid_txt, file, indent=2)

    return None

if __name__ == "__main__":
    video_list = []
    # main()
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    api_service_name = "youtube"
    api_version = "v3"
    # client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    # client_secrets_file, scopes)
    # credentials = flow.run_console()
    # youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=cfg['api_key'])
    channel_id = get_channel_id()
    uploads_playlist_id = get_uploads_list(channel_id)
    videos_list = get_video_list(uploads_playlist_id)
    output_text(videos_list)
    # print("An HTTP error  occurred")