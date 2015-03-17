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

# C'est la profondeur du graphe qui influence sur le temps d'éxecution, mais la profondeur du graphe n'est elle 
# pas plus importante que le nombre de vidéos récupérée à chaque itération ? 
#(maxDepth,numberOfRelated) | time 

# (2,5)  | 0.6s 
# (2,10) | 0.7s

# (3,5)  | 2.9s
# (3,10) | 2.62s

# (4,5)  | 16.3s
# (4,10) | 17.02s

maxDepth=2
numberOfRelated = 4
maxIdAPI = 50

# FIND RELATED VIDEOS FROM A SPECIFIC ONE 
def getVideoRelated (depth, VideoID):

	related_video_api ="https://www.googleapis.com/youtube/v3/search?relatedToVideoId="+str(VideoID)+"&type=video&maxResults="+str(numberOfRelated)+"&key="+str(api_key)+"&part=id"

	try:
		inp = urllib.urlopen(related_video_api)
		
		respRelated=json.load(inp)
		inp.close()

		# relatedVideosID : list of related video from a specific one 
		for x in xrange(0,len(respRelated['items'])):
			videosId.append([depth,respRelated['items'][x]['id']['videoId']])

	except Exception, err:
		print "error when trying to get the ID of related videos"

# SAVE DATA FROM A LIST OF VIDEO ID 
def getVideoData (finalId):
	
	# Mettre à la chaine tous les ID et taper une seule fois dans l'URL (limitation à 50)
	nbList = len(finalId)/maxIdAPI
	allID =[]
	i = 0 

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
		
		# try:
		# 	inp = urllib.urlopen(api)
		# 	resp=json.load(inp)
		# 	inp.close()

		# 	for y in xrange(0,maxIdAPI-1):
				
		# 		videoLevel = finalId[i][0]
					
		# 		commentCount = resp['items'][y]['statistics']['commentCount']
		# 		viewCount = resp['items'][y]['statistics']['viewCount']
		# 		favoriteCount = resp['items'][y]['statistics']['favoriteCount']
		# 		likeCount = resp['items'][y]['statistics']['likeCount']
		# 		dislikeCount = resp['items'][y]['statistics']['dislikeCount']
		# 		videoName = resp['items'][y]['snippet']['title']
		# 		videoUrl = f.get_url(videoID)


		# 		current = v.video(videoLevel,videoID, videoName, videoUrl, viewCount, commentCount, likeCount, dislikeCount, relatedVideo)
		# 		videosData.append(current)

		# except Exception, err:
			# print "error when trying to get the data from the ID list"

def getAllID(ID, depth):
	
	if (depth==maxDepth):
		return

	depth+=1
	getVideoRelated(depth,ID)	

	BORNINF,BORNSUP = maxDepth*(depth-1), maxDepth*depth 

	for x in xrange(BORNINF, BORNSUP):
		getAllID(videosId[x][1],depth)

def comp(E1,E2):
    if E1[0]<E2[0]:
        return -1
    if E1[0]>E2[0]:
        return 1
    return 0
 

	
def main():
	# url = 'https://www.youtube.com/watch?v=sFrNsSnk8GM'
	url='https://www.youtube.com/watch?v=2HIuN5lxMCI'
	initialID = f.get_id(url)
	
	getAllID(initialID,0)
	finalId = [[0,initialID]] + videosId
	# finalId.sort(comp, reverse=False)
	
	print finalId
	print len(finalId)
	# getVideoData(finalId)




if __name__ == '__main__':
	main()




