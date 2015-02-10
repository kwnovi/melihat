# -*- coding: utf-8 -*-
#CLASSE VIDÉO

class video:
	def __init__(self,level,videoID,title, url, views, comments, likes, dislikes):
		self.level= level
		self.id = videoID 
		self.title = title
		self.url = url
		self.views = views
		self.comments = comments
		self.likes = likes
		self.dislikes = dislikes

	def show(self): 
		 s=( "Level : " + str(self.level) + "\n"+
		 		"ID : " + str(self.id) + "\n" +
				 "Title : " + str(self.title) + "\n"+
				 "URL : " + str(self.url) + "\n"+
				 "Views : " + str(self.views) + "\n"+
				 "Comments : " + str(self.comments) + "\n"+
				 "Likes : " + str(self.likes) + "\n"+
				 "Dislikes : " + str(self.dislikes) + "\n")
		 print s



#TEST
def main():
	t = video(0,"DhfjeLjxn33","Task Rok - May Flowers", "https://www.youtube.com/", 333, 23,134,43)
	t.show()
	

if __name__ == '__main__':
	main()

