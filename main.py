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

maxDepth=3
numberOfRelated = 3
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
	lenghAllID =[]
	i = 0

	#creer les videos avec les bons ID avant de remplir les renseignements
	for x in xrange(0,len(finalId)):
		current = v.video(finalId[x][0],finalId[x][1], "", "", 0, 0, 0, 0)
		videosData.append(current)

	for x in xrange(0, nbList+1):
		allID.append("")
		lenghAllID.append("")
		
		BORNINF, BORNSUP = maxIdAPI*x, maxIdAPI*(x+1)
		for y in range(BORNINF,BORNSUP):
			if (y<len(finalId)):
				if (y%maxIdAPI==0):
					allID[x]+=finalId[y][1]
					lenghAllID[x]=1
				else:
					allID[x]+=","+finalId[y][1]
					lenghAllID[x]+=1
	
		api = 'https://www.googleapis.com/youtube/v3/videos?id='+str(allID[x])+'&key='+str(api_key)+'&part=snippet,statistics'
		# print allID[x]
		# print  'lenghAllID '+str(x)+' : ' + str(lenghAllID[x])
		try:
			inp = urllib.urlopen(api)
			resp=json.load(inp)
			inp.close()


			for y in xrange(0,lenghAllID[x]): #nombre d'ID dans allID[x]
				videosData[i].comments = resp['items'][y]['statistics']['commentCount']
				videosData[i].views = resp['items'][y]['statistics']['viewCount']
				videosData[i].likes = resp['items'][y]['statistics']['likeCount']
				videosData[i].dislikes = resp['items'][y]['statistics']['dislikeCount']
				videosData[i].title = resp['items'][y]['snippet']['title']
				videosData[i].url = f.get_url(videosData[i].id)
				# print i
				i+=1


		except Exception, err:
			print "error when trying to get the data from the ID list"
# CONSTRUCTION OF THE IDs GRAPH
def getAllID(depth,ID):
	
	if (depth==maxDepth):
		return

	childs = getVideoRelated(depth,ID)

	for x in range(0,len(childs)):
		videosId.append([childs[x][0], childs[x][1]])
		getAllID(childs[x][0]+1, childs[x][1])

def maxLikes (depth): 
	concernData = []

	for x in xrange(0,len(videosData)):
		if (videosData[x].level == depth):
			concernData.append(videosData[x])

	return max(concernData, key = lambda x: x.likes)

			
def main():

	url='https://www.youtube.com/watch?v=M1hYcein2-Y'
	initialID = f.get_id(url)

	videosId.append([0,initialID])
	getAllID(1,initialID)

	getVideoData(videosId)

	maxLikes(2)


if __name__ == '__main__':
	main()




