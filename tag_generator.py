from image_processor import ImgObj
from crawler import crawl_img
import math
from color_library import colors
from copy import deepcopy

"""
Takes in specific Tumblr page, list of possible tags and number of images that need tags.
Does a google image search on tag words and develops a color profile for each.
Compares images from Tumblr to tag color profiles to automatically assign tags to Tumblr pictures.
"""

#Returns a dictionary of picture URLs from a specific Tumblr page with matching tags from the list of tag words provided.
def tag_gen(tumblr_url,list_of_tags,number_pics):
    
    #Get average color profile for all tags
    word_avg = {}
    for word in list_of_tags:
        listlinks = crawl_img(1,0,word) 
        list_obj = []
        for link in listlinks:
            list_obj = list_obj + [ImgObj(link)]
        avg_col = get_averages(list_obj)
        word_avg[word] = avg_col
    
    tumblr_tags = {}
    tumblr_imgs = crawl_img(0,number_pics,tumblr_url)
    for link in tumblr_imgs:
        tumblr_tags[link] = []
        
    #Compare image with tags and assign relevant tags
    for link in tumblr_imgs:
        tumb_obj = ImgObj(link)
        tumb_colors = tumb_obj.get_colors()       
        for tag in word_avg:       
            if is_similar(word_avg[tag],tumb_colors):
                tumblr_tags[link] = tumblr_tags[link] + [tag]
    return tumblr_tags

#Compares two color profiles and returns True if similar.
def is_similar(dict_search,list_tumblr):
    
    threshold = 100
    differences = 0
    for entry in list_tumblr:
        color = entry[0]
        differences += abs(dict_search[color]-entry[1])
    if differences<=threshold:
        return True
    return False


#Takes in a group of image objects and returns their average color profile 
def get_averages(img_objects):
    
    avg_colors = deepcopy(colors)
    for entry in avg_colors:
        avg_colors[entry] = 0.0
        
    number_obj = len(img_objects)
    len_colors = len(avg_colors)

    #calculate sums
    for entry in img_objects:
        current = entry.get_colors()
        if current != None:
            for i in range(len_colors):
                current_color = current[i][0]
                avg_colors[current_color] += current[i][1]
        else:
            number_obj = number_obj-1
            
    #take averages
    for entry in avg_colors:
        avg_colors[entry] = avg_colors[entry]/number_obj
    
    return avg_colors


"""
#Example words,tumblr

list_of_words = ["love","romantic","calm","happy","depressed","angry","elegant","feminine"]
tumblr = "http://sunshine-on-earth.tumblr.com/"
print tag_gen(tumblr,list_of_words,8)

"""