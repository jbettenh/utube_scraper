#! python 3
# This will save all video titles from a YouTube channel to a text file.

import os
import yaml
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


def get_auth_service():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    # client_secrets_file, scopes)
    # credentials = flow.run_console()

    return build(API_SERVICE_NAME, API_VERSION, developerKey=cfg['api_key'])


def get_channel_id():
    # Ask for channel name
    channels = []
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
            channels = {'channel_title': search_result['snippet']['title'], 'channel_id': search_result['id']['channelId']}
            print('Found Channel: ' + channels['channel_title'])
        return channels

    return None


def get_uploads_list(fnd_id):
    # Get Uploads ID
    uploads_response = youtube.channels().list(
        part="contentDetails",
        id=fnd_id
    ).execute()

    for uploads_result in uploads_response.get('items', []):
        if uploads_result['kind'] == 'youtube#channel':
            return uploads_result['contentDetails']['relatedPlaylists']['uploads']
    return None


def get_video_list(uploads_id):
    videos = []
    next_page_token = ''
    print('Upload ID: ' + uploads_id)
    print('Next page token: \n')
    # Get video upload list
    while next_page_token is not None:
        video_response = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for video_result in video_response['items']:
            if video_result['kind'] == 'youtube#playlistItem':
                videos.append(video_result['snippet']['title'])
        next_page_token = video_response.get('nextPageToken')

        print(next_page_token)
    return videos


def output_text(vid_txt):
    # List titles in file
    with open('videos.txt', 'w') as file:
        json.dump(vid_txt, file, indent=2)

    return None


if __name__ == "__main__":
    video_list = []
    channel_info = []
    youtube = get_auth_service()

    channel_info = get_channel_id()


    try:
        channel_info['uploads_id'] = get_uploads_list(channel_info['channel_id'])
        if channel_info['uploads_id']:
            channel_info['videos'] = get_video_list(channel_info['uploads_id'])
            #videos_list = get_video_list(channel_info['uploads_id'])
            output_text(channel_info)
            print('Video list written to file.')
        else:
            print('There is no uploaded videos playlist for this user.')
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))