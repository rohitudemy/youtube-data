#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import csv
import json
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def udemy_youtube(options):
    DEVELOPER_KEY = options.key
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    output = "youtube_" + timestr + ".csv"
    q = open(options.file, "rb")
    f = open(output, "w+")

    qr = csv.reader(q)
    wr = csv.writer(f)

    wr.writerow(['keyword', 'id', 'title', 'channel_id', 'channel_title', 'published_date', 'description',
                 'views', 'likes', 'dislikes', 'comment_count', 'rank'])

    description = []
    views = []
    likes = []
    dislikes = []
    comments = []
    rank = 1
    keywords_remaining = sum(1 for row in qr)
    q.seek(0)

    for row in qr:

        keyword = ''.join(row)

        search_response = youtube.search().list(
            q=keyword,
            part="id,snippet",
            maxResults=options.max
        ).execute()

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                ids = search_result["id"]["videoId"]
                title = search_result["snippet"]["title"]
                published_date = search_result["snippet"]["publishedAt"]
                channel_id = search_result["snippet"]["channelId"]
                channel_title = search_result["snippet"]["channelTitle"]

                video_response = youtube.videos().list(
                    id=search_result["id"]["videoId"],
                    part="snippet,statistics"
                ).execute()

                for video_stats in video_response.get("items", []):
                    try:
                        description = video_stats["snippet"]["description"]
                        views = video_stats["statistics"]["viewCount"]
                        likes = video_stats["statistics"]["likeCount"]
                        dislikes = video_stats["statistics"]["dislikeCount"]
                        comments = video_stats["statistics"]["commentCount"]
                    except KeyError:
                        comments = 0

                wr.writerow([keyword, ids, title, channel_id, channel_title, published_date, description,
                             views, likes, dislikes, comments, rank])
                rank += 1

        rank = 1
        keywords_remaining -= 1
        print 'Keywords Remaining: %s' % keywords_remaining

    f.close()
    q.close()


if __name__ == "__main__":
    argparser.add_argument("--file", help="File name", default="queries.csv")
    argparser.add_argument("--max", help="Max results", default=25)
    argparser.add_argument("--key", help="Developer Key", default="YOUR_KEY_HERE")
    args = argparser.parse_args()

    try:
        udemy_youtube(args)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
