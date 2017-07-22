
#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import csv
import json
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')


DEVELOPER_KEY = "AIzaSyAiWWxMUwCr7ggubQU_qo4rBOWDj-sB5m4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  f = open("youtube.csv", "w+")
  q = open("queries.csv", "rb")

  wr = csv.writer(f)
  qr = csv.reader(q)

  wr.writerow(['keyword','id','title','channel_id','channel_title','published_date','description',
               'views','likes','dislikes','comment_count'])


  ids = []
  title = []
  published_date = []
  videos = []
  channel_id = []
  channel_title = []
  description = []
  
  views = []
  likes = []
  dislikes = []
  comments = []
  

  for row in qr:

    keyword = ''.join(row)

    search_response = youtube.search().list(
      q=keyword,
      part="id,snippet",
      maxResults=options.max_results
    ).execute()

    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        ids = search_result["id"]["videoId"]
        title = search_result["snippet"]["title"]
        published_date = search_result["snippet"]["publishedAt"]
        channel_id = search_result["snippet"]["channelId"]
        channel_title = search_result["snippet"]["channelTitle"]
        description = search_result["snippet"]["description"]

        video_response = youtube.videos().list(
          id = search_result["id"]["videoId"],
          part = "statistics"
          ).execute()
        
        for video_stats in video_response.get("items", []):
          try:
            views = video_stats["statistics"]["viewCount"]
            likes = video_stats["statistics"]["likeCount"]
            dislikes = video_stats["statistics"]["dislikeCount"]
            comments = video_stats["statistics"]["commentCount"]
          except KeyError:
            comments = 0

        wr.writerow([keyword, ids, title, channel_id, channel_title, published_date, description, views, likes, dislikes, comments])
  

  f.close()
  q.close()

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
