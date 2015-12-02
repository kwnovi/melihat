# -*- coding: utf-8 -*-

from flask import *
from urlparse import urlparse
import urllib
import  json 
import csv
import time

app = Flask(__name__)

api_key = 'YOUR API KEY'
videosData, videosId = [], []

maxIdAPI = 50

class video:
	def __init__(self,level,videoID,title, url, views, comments, likes, dislikes,popularite,occurence):
		self.level= level
		self.id = videoID
		self.title = str(title).encode('utf-8')
		self.url = url
		self.views = views
		self.comments = comments
		self.likes = likes
		self.dislikes = dislikes
		self.popularite = popularite
		self.occurence = occurence

def get_id(value):
	"""
	Retourne l'ID d'une vidéo YouTube à partir d'un lien
	
	Formats valides :

	- http://youtu.be/5VtsTW_t9xk
	- http://www.youtube.com/embed/5VtsTW_t9xk"
	- http://www.youtube.com/v/5VtsTW_t9xk?version=3&amp;hl=en_US"
	- https://www.youtube.com/watch?v=5VtsTW_t9xk"

	"""
	query = urlparse(value)

	if query.hostname=="youtu.be":
		return query.path[1:]
	if query.hostname in ('www.youtube.com', 'youtube.com'):
		if query.path == "/watch":
			return query.query[2:]
		if (query.path[:7] == "/embed/" or query.path[:3] == "/v/") :
			return query.path.split("/")[2]
	return None

def get_url(value):
	"""
	Retourne l'url d'une vidéo YouTube à partir de son ID
	"""
	return 'www.youtube.com/watch?v='+str(value)

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

def getVideoData (finalId):
	
	# Mettre à la chaine tous les ID et taper une seule fois dans l'URL (limitation à 50)
	nbList = len(finalId)/maxIdAPI
	allID =[]
	lenghAllID =[]
	i = 0

	#creer les videos avec les bons ID avant de remplir les renseignements
	for x in xrange(0,len(finalId)):
		current = video(finalId[x][0],finalId[x][1], "", "", 0, 0, 0, 0, 0, 0)
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

		try:
			inp = urllib.urlopen(api)
			resp=json.load(inp)
			inp.close()


			for y in xrange(0,lenghAllID[x]): 
				videosData[i].comments = resp['items'][y]['statistics']['commentCount']
				videosData[i].views = resp['items'][y]['statistics']['viewCount']
				videosData[i].likes = resp['items'][y]['statistics']['likeCount']
				videosData[i].dislikes = resp['items'][y]['statistics']['dislikeCount']
				videosData[i].title = resp['items'][y]['snippet']['title']
				videosData[i].url = get_url(videosData[i].id)

				i+=1


		except Exception, err:
			print "error when trying to get the data from the ID list"

def getAllID(depth,ID):
	
	if (depth==maxDepth):
		return

	childs = getVideoRelated(depth,ID)

	for x in range(0,len(childs)):
		videosId.append([childs[x][0], childs[x][1]])
		getAllID(childs[x][0]+1, childs[x][1])

def mostPopularVideo(): return max(videosData, key=lambda v: int(v.popularite))

def mostFrequentVideo(): return max(videosData, key=lambda v: int(v.occurence))

def crawling(url,maxDepth,numberOfRelated):
	
	start = time.time()

	initialID = get_id(url)

	videosId.append([0,initialID])
	getAllID(1,initialID)

	getVideoData(videosId)

	populariteInitialVid = (((float(videosData[0].likes)+1)/(float(videosData[0].dislikes)+1))*(float(videosData[0].comments)+1))

	for x in xrange(0,len(videosData)):
		if (x==0):
			videosData[x].popularite = 100
		else:
			popularite = (((float(videosData[x].likes)+1)/(float(videosData[x].dislikes)+1))*(float(videosData[x].comments)+1))
			videosData[x].popularite = round((popularite/populariteInitialVid)*100,1)
		for y in xrange(0,len(videosData)):
			if (videosData[x].title==videosData[y].title or videosData[x].id==videosData[y].id) :
				videosData[x].occurence +=1


	with open('data.csv','wb') as csvData:
		dataWriter = csv.writer(csvData, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
		dataWriter.writerow(['Depth']+['ID']+['Title']+['Popularity']+['Occurency'])
		for x in xrange(0,len(videosData)):
			dataWriter.writerow([videosData[x].level]+[videosData[x].id]+[videosData[x].title.encode("utf-8")]+[videosData[x].popularite]+[videosData[x].occurence])

	timeExecution = round(time.time() - start,1)
	mostFrequent = mostFrequentVideo()
	mostPopular = mostFrequentPopular()
	values = [videosData[0], mostPopular, mostFrequent, len(videosData), timeExecution]

@app.route('/')
def main():

	global maxDepth, numberOfRelated

	url='https://www.youtube.com/watch?v=t5747BhezKM'
	maxDepth= 2
	numberOfRelated =2

	values = crawling(url,maxDepth,numberOfRelated)

	start = True 

	if start:
		return render_template('initial.html')
	else:
		return render_template('index.html',var=values)


if __name__ == "__main__":
    app.run(debug=True)

