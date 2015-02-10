#  # -*- coding: utf-8 -*-
from lib import video as v 
from lib import function  as f 
import urllib
import  json 
import sys
import argparse
import logging

#INITIALISATION

videosData = []
relatedVideosID = []
findAll = False

#URL DE LA VIDEO DE DÉPART
url = YOUR_URL
api_key = YOUR_API_KEY

videoID = f.get_id(url)
api = 'https://www.googleapis.com/youtube/v3/videos?id='+str(videoID)+'&key='+str(api_key)+'&part=snippet,statistics'

inp = urllib.urlopen(api)
resp=json.load(inp)
inp.close()

# DATA CROWLING

videoLevel = 0
commentCount = resp['items'][0]['statistics']['commentCount']
viewCount = resp['items'][0]['statistics']['viewCount']
favoriteCount = resp['items'][0]['statistics']['favoriteCount']
likeCount = resp['items'][0]['statistics']['likeCount']
dislikeCount = resp['items'][0]['statistics']['dislikeCount']
videoName = resp['items'][0]['snippet']['title']
videoUrl = f.get_url(videoID)

current = v.video(videoLevel,videoID, videoName, videoUrl, viewCount, commentCount, likeCount, dislikeCount)
videosData.append(current)


related_video_api ="https://www.googleapis.com/youtube/v3/search?relatedToVideoId="+str(videoID)+"&type=video&maxResults=50&key="+str(api_key)+"&part=id"
inp = urllib.urlopen(related_video_api)
respRelated=json.load(inp)
inp.close()

for x in xrange(0,50):
	relatedVideosID.append(respRelated['items'][x]['id']['videoId'])




