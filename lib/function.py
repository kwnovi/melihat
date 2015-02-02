# -*- coding: utf-8 -*-
from urlparse import urlparse

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

# DEF IMPORT_JSON
# DEF BROWSE_SUGGGESTION


#TEST
def main():
	url, url2, url3, url4 ="http://youtu.be/5VtsTW_t9xk","http://www.youtube.com/embed/5VtsTW_t9xk","http://www.youtube.com/v/5VtsTW_t9xk?version=3&amp;hl=en_US","https://www.youtube.com/watch?v=5VtsTW_t9xk"
	for x in (url, url2, url3, url4):
		print get_id(x)

if __name__ == '__main__':
	main()
