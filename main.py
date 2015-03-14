# -*- coding: utf-8 -*-
from lib import video as v 
from lib import function  as f 
import urllib
import  json 
import sys
import argparse
import logging

api_key = 'AIzaSyCHeAL8UhXDgvE3YJ45_dkEasCQ3qy16TM'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

videosData = []
videosId = []
maxDepth=2
numberOfRelated = 5

# FIND RELATED VIDEOS FROM A SPECIFIC ONE 
# INPUT : videoID (string)
# OUPUT : relatedVideo (list of string)
def getVideoRelated (depth, VideoID):

	related_video_api ="https://www.googleapis.com/youtube/v3/search?relatedToVideoId="+str(VideoID)+"&type=video&maxResults="+str(numberOfRelated)+"&key="+str(api_key)+"&part=id"
	
	print related_video_api

	if (depth==1):
		print related_video_api
	try:
		inp = urllib.urlopen(related_video_api)
		
		respRelated=json.load(inp)
		inp.close()

		# relatedVideosID : list of related video from a specific one 
		for x in xrange(0,len(respRelated['items'])):
			videosId.append([depth,respRelated['items'][x]['id']['videoId']])

	except Exception, err:
		print "error when trying to get the ID of related videos"

# SAVE DATA FROM ONE VIDEO

def getVideoData (videoID, videosData, videoDepth):
	
	api = 'https://www.googleapis.com/youtube/v3/videos?id='+str(videoID)+'&key='+str(api_key)+'&part=snippet,statistics'
	
	try:
		inp = urllib.urlopen(api)
		resp=json.load(inp)
		inp.close()

		videoLevel = videoDepth

		commentCount = resp['items'][0]['statistics']['commentCount']
		viewCount = resp['items'][0]['statistics']['viewCount']
		favoriteCount = resp['items'][0]['statistics']['favoriteCount']
		likeCount = resp['items'][0]['statistics']['likeCount']
		dislikeCount = resp['items'][0]['statistics']['dislikeCount']
		videoName = resp['items'][0]['snippet']['title']
		videoUrl = f.get_url(videoID)

		relatedVideo = getVideoRelated(videoID)

		current = v.video(videoLevel,videoID, videoName, videoUrl, viewCount, commentCount, likeCount, dislikeCount, relatedVideo)
		videosData.append(current)

		return current

	except Exception, err:
		print "error when trying to get the data from a specific video"

def getAllID(ID, depth):

	if (depth==maxDepth):
		return

	depth+=1
	getVideoRelated(depth,ID)

	BORNINF,BORNSUP = maxDepth*(depth-1), maxDepth*depth 

	for x in xrange(BORNINF,BORNSUP):
		getAllID(videosId[x][1],depth)


	
def main():
	# url = 'https://www.youtube.com/watch?v=sFrNsSnk8GM'
	url='https://www.youtube.com/watch?v=2HIuN5lxMCI'
	initialID = f.get_id(url)

	videosId.append([0,initialID])
	getAllID(initialID,0)
	
	print videosId
	print len(videosId)

	# print len(videosData[0].relatedVideos)
	# print videosData[0].relatedVideos[0]
	# test =  videosData[0].relatedVideos[1]
	# print 'https://www.googleapis.com/youtube/v3/videos?id='+str(test)+'&key='+str(api_key)+'&part=snippet,statistics'
	


if __name__ == '__main__':
	main()




