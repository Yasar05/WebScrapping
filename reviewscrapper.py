from bs4 import  BeautifulSoup as bs
from urllib.error import HTTPError,URLError
from urllib.request import urlopen as uReq
import re

import csv
csv_file = open('ebayreviews.csv','w',encoding='utf-8')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Product','Author','Rating','Title','Comment'])

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
     ebay_html = bs(ebayPage,'html.parser')  #ebay product landing page
     badContent = ebay_html.find("nonExistingTag")
except AttributeError as e:
     print('Tag was not found')

try:
    review_items=ebay_html.find("div",class_="s-item__reviews")
except:
    print('Class not found')
try:
    reviews_page=uReq(review_items.a['href']) # user-reviews link
    reviews_html=bs(reviews_page.read(),"html.parser")
except:
    print('Link not found')

try:
    all_reviews = reviews_html.find('div',class_="see--all--reviews")
    totrev = all_reviews.a.text
    try:
        r=re.search(r'\d+',totrev) ##extracting number of reviews using regex
        total_reviews=int(r.group(0))
        totalpages=round(total_reviews/10) ##calculating no of pages for paginataion
    except:
        totalpages=1

except Exception as e:
    print('Requested page not found')

try:
    all_reviews_page=uReq(all_reviews.a["href"])
    all_reviews_html=bs(all_reviews_page.read(),'html.parser')
except:
    print('Page not found')

page=1
while(page <= totalpages):

    all_user_reviews = all_reviews_html.find_all('div', class_='ebay-review-section')

    for review in all_user_reviews:
        try:
            reviews_rating=review.find('div',class_="ebay-star-rating")
            rating=reviews_rating.span["aria-label"]
        except:
            rating='rating not available'

        try:
            author=review.find('div',class_="ebay-review-section-l").a['title']
        except:
            author='No name'

        try:

            body=review.find('div',class_='ebay-review-section-r')
            body_text=body.p.text
        except:
            body_text='No comments'

        try:
            title = body.h3.text
        except:
            title='No title'

        csv_writer.writerow([searchString,author,rating,title,body_text])
    if page > 1:
        next_page_link = firstpagelink+'?pgn='+str(page)

    else:
        pages = all_reviews_html.find('ul', class_="small pagination")
        base_link = pages.li.find('a', class_="spf-link")
        firstpagelink = base_link['href']

    if page == 1:
        nextpage=uReq((firstpagelink))
    else:
        nextpage = uReq(next_page_link)

    if nextpage is not None:
        all_reviews_html = bs(nextpage.read(), "html.parser")
        page = page+1
    else:
        break

print("csv file created sucessfully with the reviews")
csv_file.close()