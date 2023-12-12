import datetime
import psycopg2
from googleapiclient.discovery import build
from configparser import ConfigParser

# Load configuration from file
config = ConfigParser()
config.read('config.ini')

# YouTube API configuration
api_key = config.get('youtube', 'api_key')
youtube = build('youtube', 'v3', developerKey=api_key)

# PostgreSQL database configuration
host = config.get('database', 'host')
user = config.get('database', 'user')
password = config.get('database', 'password')
database = config.get('database', 'database')
port = 5432


# Get today's date in ISO 8601 format (YYYY-MM-DD)
today_date = datetime.date.today().isoformat()

# SQL statement to create the table
# publish_date given in ISO 8601 format (YYYY-MM-DD)
# duration given in ISO 8601 duration format (PT#M#S, PT#H#M#S etc)
create_table_query = """
CREATE TABLE IF NOT EXISTS youtube_metrics (
    video_id VARCHAR(20),
    trending_date DATE,
    publish_date DATE,
    title VARCHAR(255),
    duration INTERVAL,
    views INTEGER,
    likes INTEGER,
    comments INTEGER,
    PRIMARY KEY (video_id, trending_date)
);
"""

# SQL statement to insert data into the table
insert_data_query = """
INSERT INTO youtube_metrics (video_id, trending_date, publish_date, title, duration, views, likes, comments)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (video_id, trending_date) DO NOTHING;
"""

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()

def get_trending_videos():
    # Retrieve trending videos
    trending_videos = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        chart='mostPopular',
        regionCode='US',
        maxResults=50
    ).execute()

    return trending_videos['items']

def store_in_database(conn, video_data):
    cursor = conn.cursor()

    # Insert data into PostgreSQL
    for video in video_data:
        video_id = video['id']
        title = video['snippet']['title']
        publish_date = video['snippet']['publishedAt']
        duration = video['contentDetails']['duration']
        views = video['statistics']['viewCount']
        likes = video['statistics']['likeCount']
        # If comments are disabled, set count to -1
        comments = video['statistics'].get('commentCount', -1)

        # Execute the query to insert data into the table
        cursor.execute(insert_data_query, (video_id, today_date, publish_date, title, duration, views, likes, comments))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()


# def lambda_handler(event, context):
if __name__ == "__main__":
    conn = None # Declare conn as a global variable

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(dbname=database, user=user, password=password, host=host, port=port)

        # Step 1: Create the table (if it doesn't exist)
        create_table(conn)

        # Step 2: Get trending videos from YouTube API
        trending_videos_data = get_trending_videos()

        # Step 3: Store data in the PostgreSQL database
        if trending_videos_data:
            store_in_database(conn, trending_videos_data)
            print("Data successfully stored in the database.")
        else:
            print("No trending videos data retrieved.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()
