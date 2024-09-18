import os
import googleapiclient.discovery

#Set up the API key
api_key = 'AIzaSyCrUgIJak68cYM4AEA-O3JB-Yz-9pDwhfw'

# Create a YouTube resource object
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

def search_videos(query):
    # Make the API request
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=5  # number of videos that you want
    )
    response = request.execute()

    # Retrieve video details
    videos = []
    for item in response['items']:
        video = {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
        }
        videos.append(video)

    return videos

# Get search query from the user
search_query = input('Enter your search query: ')

# Search for videos
search_results = search_videos(search_query)

# Display the results
for video in search_results:
    print('Title:', video['title'])
    #print('Video ID:', video['video_id'])
    print('https://www.youtube.com/watch?v=' + video['video_id'])
    print()
