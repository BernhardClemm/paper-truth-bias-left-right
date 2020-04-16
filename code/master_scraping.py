###########################
###########################
### Scraping news items ###
###########################
###########################

import csv
import sys
from datetime import datetime

# General parameters ####

sys.path.append('/Users/bernhardclemm/Dropbox/PhD/Papers/2020 Bias Left Right/Operationalization/Stimulus')

startdate_string = "1 July 2019 00:00:00"
startdate = datetime.strptime(startdate_string, '%d %B %Y %H:%M:%S')

###########
# Reuters #
###########

# Manually find ID you want to start at

itemid = "1586462555054695000"  

# Call function 

from reuters import reuters_scraping

reuters_list = reuters_scraping(startdate, itemid)

##########
# Snopes #
##########

# Ratings of Snopes fact checks: https://www.snopes.com/fact-check-ratings/
## To be included as true news: "True", "correct attribution"
## To be included as false news: "False", "misattribution"
## Not included: "Mixture", "unproven", "outdated", "miscaptioned", "scam", "legend", "labeled satire", "lost legend"

# CSS classes of ratings

ratingstrue = ["fact_check_rating-true", "fact_check_rating-correct-attribution"]
ratingsfalse = ["fact_check_rating-false", "fact_check_rating-misattributed"]

# Call function 

from snopes import snopes_scraping

snopes_list = snopes_scraping(startdate, ratingstrue, ratingsfalse)

##############
# Politifact #
##############

ratingstrue = ["true"]
ratingsfalse = ["false","pants-fire"]

types_all = ["YouTube videos", 
         "Facebook posts", 
         "Bloggers", 
         "Viral image",
         "Instagram posts",
         "Chain message",
         "Tweets"]

# Call function 

from politifact import politifact_scraping

politifact_list = politifact_scraping(startdate, ratingstrue, ratingsfalse, types_all)

##################
# TruthorFiction #
##################

# Ratings
## To be included as true: 'True'
## To be included as false: 'Not True'
## Not included: 'Unknown', 'Mixed', 'Decontextualized'

ratingstrue = ["True"]
ratingsfalse = ["Not True"]

types_all = ["Fact Checks"]

# Call function 

from truthorfiction import truthorfiction_scraping

truthorfiction_list = truthorfiction_scraping(startdate, ratingstrue, ratingsfalse, types_all)

########################
# Eliminate duplicates #
########################



####################
# Combine all sets #
####################

# Extract necessary information from Reuters JSON

reuters_list_new = []
for item in reuters_list:
    link = item["templates"][0]["story"]["url"]
    date = item["templates"][0]["story"]["updated_at"]
    title = item["templates"][0]["story"]["hed"]
    teaser = item["templates"][0]["story"]["lede"]
    item_type = item["templates"][0]["primary_channel"]["name"]
    item_id = item["wireitem_id"]
    item_dict = {"id": item_id, 
                 "link" : link,
                 "date" : date, 
                 "title" : title,
                 "teaser": teaser,
                 "truth" : "true",
                 "source" : "Reuters",
                 "type" : item_type}
    reuters_list_new.append(item_dict)
    
# Combine lists

list_all = snopes_list + politifact_list + truthorfiction_list + reuters_list_new

keys = list_all[0].keys()
with open('news_items.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(list_all)
