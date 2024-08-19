from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Step 1: Define the scope for YouTube Data API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Step 2: Set up the OAuth 2.0 flow
def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)  # This will open a browser window for OAuth

    # Save the credentials for the next run
    with open('token.json', 'w') as token_file:
        token_file.write(creds.to_json())
    
    return creds

# Step 3: Initialize the YouTube API client
def get_youtube_service():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token_file:
            creds = json.load(token_file)

    if not creds:
        creds = authenticate()

    service = build('youtube', 'v3', credentials=creds)
    return service

# Step 4: Fetch YouTube history data (sample data fetch for recent activities)
def fetch_youtube_history(service, days):
    now = datetime.utcnow().isoformat("T") + "Z"  # 'Z' indicates UTC time
    past = (datetime.utcnow() - timedelta(days=days)).isoformat("T") + "Z"

    request = service.activities().list(
        part='snippet,contentDetails',
        mine=True,
        maxResults=50,  # You can adjust this number based on your needs
        publishedAfter=past,
        publishedBefore=now
    )
    response = request.execute()
    return response

# Step 5: Process and calculate statistics from the fetched data
def process_data(response):
    watch_time_by_day = defaultdict(int)
    total_videos = 0

    for item in response.get('items', []):
        if 'contentDetails' in item and 'upload' in item['contentDetails']:
            # Extracting video publish date
            publish_date = item['snippet']['publishedAt']
            date_obj = datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%SZ")

            # Assuming an average watch time of 5 minutes per video as a placeholder
            watch_time_by_day[date_obj.date()] += 5
            total_videos += 1

    # Print the stats
    print("YouTube Watch Statistics:")
    print(f"Total videos watched: {total_videos}")
    for day, minutes in sorted(watch_time_by_day.items()):
        print(f"{day}: {minutes} minutes")

    avg_watch_time = sum(watch_time_by_day.values()) / len(watch_time_by_day) if watch_time_by_day else 0
    print(f"Average watch time per day: {avg_watch_time:.2f} minutes")

if __name__ == '__main__':
    youtube_service = get_youtube_service()

    # Adjust the number of days for which you want to fetch the data
    days_to_fetch = 7
    youtube_history = fetch_youtube_history(youtube_service, days_to_fetch)

    process_data(youtube_history)
