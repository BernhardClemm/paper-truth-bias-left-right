import time
from datetime import datetime
from urllib.request import urlopen
import re
import json
import random

def reuters_scraping(start_date, item_id):
    
    items_list = []
    
    earliest_date = datetime.today()

    while start_date < earliest_date:
        
        try: 
            url = "https://wireapi.reuters.com/v3/feed/url/www.reuters.com/news/us?last_ad=3&until=" + item_id
            print(url)
            r = urlopen(url)
            json_content = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
        
            items_new = json_content["wireitems"]
            items_new = [item for item in items_new if item["wireitem_type"] != "ad"]
        
            earliest_date = items_new[-1]["templates"][0]["story"]["updated_at"]
            earliest_date = re.sub(r'[TZ]', ' ', earliest_date)
            earliest_date = datetime.strptime(earliest_date, '%Y-%m-%d %H:%M:%S ')
            print(earliest_date)
            
            item_id = items_new[-1]["wireitem_id"]
        
            items_list = items_list + items_new
            
        except:
            print("error")
            time.sleep(3 + random.random())
    
    return(items_list)
           

        




