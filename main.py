#  # -*- coding: utf-8 -*-
from lib import video as v 
from lib import function  as f 


#URL DE LA VIDEO DE DÉPART
url = "https://www.youtube.com/watch?v=sFrNsSnk8GM"

t = v.video(f.get_id(url),"", url, None , None, None, None)

t.show()
