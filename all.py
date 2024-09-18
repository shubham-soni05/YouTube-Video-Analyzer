import os
import googleapiclient.discovery

api_key = 'AIzaSyCrUgIJak68cYM4AEA-O3JB-Yz-9pDwhfw'

# Create a YouTube resource object
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

def search_videos(query):
    # Make the API request
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=8 
    )
    response = request.execute()

    # Retrieve video details
    videos = []
    for item in response['items']:
        video = {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
            'likes': 0,
            'views': 0
        }
        videos.append(video)

    # Retrieve likes and views for each video
    for video in videos:
        stats_request = youtube.videos().list(
            part='statistics',
            id=video['video_id']
        )
        stats_response = stats_request.execute()

        if 'items' in stats_response:
            statistics = stats_response['items'][0]['statistics']
            video['likes'] = int(statistics.get('likeCount', 0))
            video['views'] = int(statistics.get('viewCount', 0))

    return videos

search_query = input('Enter your search query: ')

# Search for videos
search_results = search_videos(search_query)

# Sort the videos based on likes, views, and views-to-likes ratio
sorted_by_likes = sorted(search_results, key=lambda x: x['likes'], reverse=True)
sorted_by_views = sorted(search_results, key=lambda x: x['views'], reverse=True)
sorted_by_ratio = sorted(search_results, key=lambda x: x['views'] / max(x['likes'], 1), reverse=False)
sorted_by_latest_ratio = sorted(search_results, key=lambda x: x['views'] / max(x['likes'], 1), reverse=True)

# Display the video with the highest likes
if sorted_by_likes:
    highest_likes_video = sorted_by_likes[0]
    print('Video with the highest likes:')
    print('Title:', highest_likes_video['title'])
    print('https://www.youtube.com/watch?v=' + highest_likes_video['video_id'])
    print()

# Display the video with the highest views
if sorted_by_views:
    highest_views_video = sorted_by_views[0]
    print('Video with the highest views:')
    print('Title:', highest_views_video['title'])
    print('https://www.youtube.com/watch?v=' + highest_views_video['video_id'])
    print()

# Display the video with the highest views-to-likes ratio (latest search)
if sorted_by_latest_ratio:
    highest_ratio_video = sorted_by_latest_ratio[0]
    print('Video with the highest views-to-likes ratio:')
    print('Title:', highest_ratio_video['title'])
    print('https://www.youtube.com/watch?v=' + highest_ratio_video['video_id'])
    print()