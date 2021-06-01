from bs4 import  BeautifulSoup as bs
import requests
import pymongo
from urllib.request import urlopen as uReq

searchString ="iphone"
try:

    ebay_url = "https://www.ebay.com/"+searchString
    uClient = uReq(ebay_url)
    ebayPage = uClient.read()
except HTTPError as e:
    print('e')
except URLError as e:
   print('The Server could not be found')


try:
     ebay_html = bs(ebayPage,'html.parser')
     badContent = ebay_html.find("nonExistingTag") # ebay product landing page
except AttributeError as e:
     print('Tag was not found')

###mongodb  database connection
client=pymongo.MongoClient("mongodb://localhost:27017/")
database=client["ebay_reviews"]
prod_reviews=database[searchString+'reviews']


review_items=ebay_html.find("div",class_="s-item__reviews")
reviews=[]
reviews_page=uReq(review_items.a['href']) # user-reviews link
reviews_html=bs(reviews_page.read(),"html.parser")
try:
    all_reviews=reviews_html.find('div',class_="see--all--reviews")
except Exception as e:
    print('Requested page not found')



###extracting reviews from the webpage
all_reviews_page=uReq(all_reviews.a["href"])
all_reviews_html=bs(all_reviews_page.read(),'html.parser')
pages = all_reviews_html.find('nav', class_="pagination-wrapper")
pagelist = pages.find('ul', class_="large pagination")
next_page_link = pagelist.li.a['href']

while(next):
    all_user_reviews=all_reviews_html.find_all('div',class_='ebay-review-section')
    for review in all_user_reviews:
        reviews_rating=review.find('div',class_="ebay-star-rating")
        rating=reviews_rating.span["aria-label"]
        author=review.find('div',class_="ebay-review-section-l").a['title']
        body=review.find('div',class_='ebay-review-section-r')
        title=body.h3.text
        body_text=body.p.text
        mydict={'Product':'iphone','Author': author, 'Rating':rating,'Title':title,'Comment':body_text}
        prod_reviews.insert_one(mydict)
    if next_page_link is not None:
        nextpage = uReq(next_page_link)
        all_reviews_html = bs(nextpage, "html.parser")
    else:
        next = False



'''def checkExistence_DB(DB_NAME, client):
    """It verifies the existence of DB"""
    DBlist = client.list_database_names()
    if DB_NAME in DBlist:
        print(f"DB: '{DB_NAME}' exists")
        return True
    print(f"DB: '{DB_NAME}' not yet present OR no collection is present in the DB")
    return False


_ = checkExistence_DB(DB_NAME=DB_NAME, client=client)'''


 '''def checkExistence_COL(COLLECTION_NAME, DB_NAME, db):
    """It verifies the existence of collection name in a database"""
    collection_list = db.list_collection_names()

    if COLLECTION_NAME in collection_list:
        print(f"Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' exists")
        return True

    print(f"Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' does not exists OR \n\
    no documents are present in the collection")
    return False


_ = checkExistence_COL(COLLECTION_NAME=COLLECTION_NAME, DB_NAME=DB_NAME, db=dataBase)'''