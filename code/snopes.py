from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def snopes_scraping(start_date, ratings_true, ratings_false):
    
    ratings = ratings_true + ratings_false
    
    i = 1
    
    items_list = []
    
    last_date = datetime.today() 
    
    while start_date < last_date:
        
        page_number = str(i)
        url = "https://www.snopes.com/fact-check/category/politics/page/" + page_number 
        print(url)
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        page_main = soup.find("div", class_ = "card")
        page_items = page_main.find_all("a", class_ = ratings)
        
        page_items_list = []
        
        for j in range(len(page_items)):
            print(j)
        
            link = page_items[j].get("href")
        
            date_html = page_items[j].find("li", class_ = "date breadcrumb-item")
            date = date_html.get_text()
            date = date.strip()
            date = datetime.strptime(date, '%d %B %Y')
            
            title_html = page_items[j].find("h5", class_ = "title")
            title = title_html.get_text()
            
            classes = page_items[j].get("class")
            if any(item in ratings_true for item in classes) is True:
                truth = "true"
            elif any(item in ratings_false for item in classes) is True:
                truth = "false"
            else:
                truth = "NA"
                    
            item_dict = {"link" : link, 
                         "date" : date, 
                         "title" : title,
                         "truth" : truth,
                         "source" : "Snopes",
                         "type" : "Politics"}
            page_items_list.append(item_dict)
            
            last_date = date # Date of the oldest item at the end of this loop
            
        items_list.extend(page_items_list) 
        
        i = i + 1
        
    return(items_list)
         

        


