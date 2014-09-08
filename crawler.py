import requests, urllib
from BeautifulSoup import BeautifulSoup

# Returns a list of links to the images from either a Google Image Search or from a specific Tumblr page
def crawl_img(type,num_img,strings):
   
    if type: #type = 1 = Google Image Search based on key word given in "strings"
        word = strings
        url = "https://www.google.com/search?tbm=isch&q="+str(word)

        source_code = requests.get(url)
        plain_text= source_code.text
        soup = BeautifulSoup(plain_text)
        listoflinks= []
        new_list = soup.findAll('img')
        for link in new_list:
            listoflinks = listoflinks + [str(link.get('src'))]
        return listoflinks
   
    else: #type = 0 = Tumblr page from URL provided in "strings"
        url = strings
        source_code = requests.get(url)
        plain_text= source_code.text
        soup = BeautifulSoup(plain_text)
        listoflinks= []
        counter = 0
        for link in soup.findAll('img'):
            if counter == num_img:
                break
            str_link = str(link.get('src'))
            if "tumblr" in str_link and ".gif" not in str_link and ".png" not in str_link:
                listoflinks = listoflinks+[str_link]
                counter += 1
        return listoflinks
    
