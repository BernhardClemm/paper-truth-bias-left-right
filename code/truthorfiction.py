from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def truthorfiction_scraping(start_date, ratings_true, ratings_false, types):
    
    ratings = ratings_true + ratings_false

    i = 1
    
    items_list = []
    
    last_date = datetime.today() 
    
    while start_date < last_date:
                        
        page_number = str(i)
        url = 'https://www.truthorfiction.com/category/fact-checks/politics/page/' + page_number
        print(url)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')
        page_main = soup.find("div", class_ = "ast-row")
        page_items = page_main.find_all("div", class_ = "post-content")
        
        page_items_list = []
        
        for j in range(len(page_items)):
            print(j)
            
            item_type_html = page_items[j].find("span", class_ = "cat-links")
            item_types = item_type_html.get_text()
            
            if any(item in item_types for item in types):
                            
                link_html = page_items[j].find("h2", class_ = "entry-title")
                link = link_html.findChild("a")["href"]
                
                date_html = page_items[j].find("span", class_ = "published")
                date_raw = date_html.get_text().strip()
                date = datetime.strptime(date_raw, '%B %d, %Y')
                
                title_link_html = page_items[j].find("h2", class_ = "entry-title")
                title = title_link_html.get_text().strip()
            
                article_req = Request(link, headers = hdr)
                article_page = urlopen(article_req)        
                article_soup = BeautifulSoup(article_page, 'html.parser')
                article_rating_html = article_soup.find("div", class_ = "rating-description")
                truth = article_rating_html.get_text().strip()
                    
                if (truth in ratings) is True:
                
                    item_dict = {"link" : link, 
                                 "date" : date, 
                                 "title" : title,
                                 "truth" : truth,
                                 "source" : "Truthorfiction",
                                 "type" : item_types}
                    
                    page_items_list.append(item_dict)
                
        items_list.extend(page_items_list) 
            
        last_date = date 
        
        i = i + 1
        
    return(items_list)
