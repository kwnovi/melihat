# -*- coding: utf-8 -*-
from lib import video as v 
from lib import function  as f 
import urllib
import  json 
import sys
import argparse
import logging

api_key = 'YOUR_API_KEY'
videosData, videosId = [], []


#(maxDepth,numberOfRelated) | time 

# (2,5)  | 0.6s 
# (2,10) | 0.7s

# (3,5)  | 2.9s
# (3,10) | 2.62s

# (4,5)  | 16.3s
# (4,10) | 17.02s

maxDepth=4
numberOfRelated = 5
maxIdAPI = 50


# FIND RELATED VIDEOS FROM A SPECIFIC ONE 
def getVideoRelated (depth, VideoID):

	related_video_api ="https://www.googleapis.com/youtube/v3/search?relatedToVideoId="+str(VideoID)+"&type=video&maxResults="+str(numberOfRelated)+"&key="+str(api_key)+"&part=id"
	temporaryVideosId = []

	try:
		inp = urllib.urlopen(related_video_api)
		
		respRelated=json.load(inp)
		inp.close()

		# relatedVideosID : list of related video from a specific one 
		for x in xrange(0,len(respRelated['items'])):
			temporaryVideosId.append([depth,respRelated['items'][x]['id']['videoId']])



	except Exception, err:
		print "error when trying to get the ID of related videos"

	return temporaryVideosId

# SAVE DATA FROM A LIST OF VIDEO ID 
def getVideoData (finalId):
	
	# Mettre à la chaine tous les ID et taper une seule fois dans l'URL (limitation à 50)
	nbList = len(finalId)/maxIdAPI
	allID =[]

	#creer les videos avec les bons ID avant de remplir les renseignements
	for x in xrange(0,len(finalId)):
		current = v.video(finalId[x][0],0, "", "", 0, 0, 0, 0)
		videosData.append(current)

	for x in xrange(0, nbList+1):
		allID.append("")
		BORNINF, BORNSUP = maxIdAPI*x, maxIdAPI*(x+1)-1
		for y in range(BORNINF,BORNSUP):
			if (y<len(finalId)):
				if (y%maxIdAPI==0):
					allID[x]+=finalId[y][1]
				else:
					allID[x]+=","+finalId[y][1]
	
		api = 'https://www.googleapis.com/youtube/v3/videos?id='+str(allID[x])+'&key='+str(api_key)+'&part=snippet,statistics'
	
	# print allID
	# print len(allID)
		# try:
		# 	inp = urllib.urlopen(api)
		# 	resp=json.load(inp)
		# 	inp.close()

		# 	for y in xrange(0,maxIdAPI-1):
					
		# 		commentCount = resp['items'][y]['statistics']['commentCount']
		# 		viewCount = resp['items'][y]['statistics']['viewCount']
		# 		favoriteCount = resp['items'][y]['statistics']['favoriteCount']
		# 		likeCount = resp['items'][y]['statistics']['likeCount']
		# 		dislikeCount = resp['items'][y]['statistics']['dislikeCount']
		# 		videoName = resp['items'][y]['snippet']['title']
		# 		videoUrl = f.get_url(videoID)


		# except Exception, err:
		# 	print "error when trying to get the data from the ID list"

def getAllID(depth,ID):
	
	if (depth==maxDepth):
		return

	childs = getVideoRelated(depth,ID)

	for x in range(0,len(childs)):
		videosId.append([childs[x][0], childs[x][1]])
		getAllID(childs[x][0]+1, childs[x][1])

	
def main():

	url='https://www.youtube.com/watch?v=2HIuN5lxMCI'
	initialID = f.get_id(url)

	videosId.append([0,initialID])
	getAllID(1,initialID)
	
	print videosId
	print len(videosId)

	getVideoData(videosId)





if __name__ == '__main__':
	main()




