from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import re

def politifact_scraping(start_date, ratings_true, ratings_false, types):
    
    ratings = ratings_true + ratings_false

    i = 1
    
    items_list = []
    
    last_date = datetime.today() 
    
    while start_date < last_date:
                        
        page_number = str(i)
        url = 'https://www.politifact.com/factchecks/?page=' + page_number 
        print(url)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')
        page_main = soup.find("div", class_ = "o-listicle__inner")
        page_items = page_main.find_all("li", class_ = "o-listicle__item")
        
        page_items_list = []
        
        for j in range(len(page_items)):
            print(j)
            
            item_type_html = page_items[j].find("a", class_ = "m-statement__name")
            item_type = item_type_html.get_text().strip()
            
            truth = page_items[j].find('img', alt=True)["alt"]
            
            if (item_type in types and truth in ratings) is True:
                
                date_html = page_items[j].find("div", class_ = "m-statement__desc")
                date_raw = date_html.get_text().strip()
                date = re.search(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}", date_raw).group()
                date = datetime.strptime(date, '%B %d, %Y')
                
                title_link_html = page_items[j].find("div", class_ = "m-statement__quote")
                title = title_link_html.get_text().strip()
                
                link_end = title_link_html.findChild("a")["href"]
                link = "www.politifact.com" + link_end
                
                truth = page_items[j].find('img', alt=True)["alt"]
                
                item_dict = {"link" : link, 
                         "date" : date, 
                         "title" : title,
                         "truth" : truth,
                         "source" : "Politifact",
                         "type" : item_type}
                page_items_list.append(item_dict)
                
                items_list.extend(page_items_list) 
            
            date_pub_html = page_items[j].find("footer", class_ = "m-statement__footer")
            date_pub_raw = date_pub_html.get_text().strip()
            date_pub = re.search(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}", date_pub_raw).group()
            date_pub = datetime.strptime(date_pub, '%B %d, %Y')
            
            last_date = date_pub # Date of the oldest item at the end of this loop
        
        i = i + 1
        
    return(items_list)
        
        