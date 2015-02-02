# -*- coding: utf-8 -*-
#CLASSE VIDÉO

class video:
	def __init__(self, vid,title, url, views, comments, likes, dislikes):
		self.id = vid 
		self.title = title
		self.url = url
		self.views = views
		self.comments = comments
		self.likes = likes
		self.dislikes = dislikes

	def show(self): 
		 s=("ID : " + str(self.id) + "\n" +
				 "Title : " + str(self.title) + "\n"+
				 "URL : " + str(self.url) + "\n"+
				 "Views : " + str(self.views) + "\n"+
				 "Comments : " + str(self.comments) + "\n"+
				 "Likes : " + str(self.likes) + "\n"+
				 "Dislikes : " + str(self.dislikes) + "\n")
		 print s



#TEST
def main():
	t = video("Task Rok - May Flowers","DhfjeLjxn33", "https://www.youtube.com/", 333, 23,134,43)
	t.show()
	

if __name__ == '__main__':
	main()

