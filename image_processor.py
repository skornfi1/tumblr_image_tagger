from PIL import Image
from PIL import ImageFilter
import urllib, cStringIO, math
from color_library import colors
from operator import itemgetter

class ImgObj: 
    """Creates an object that has the color distribution, number of pixels and URL of the image"""

    def __init__(self,url_name):
        self.URL = url_name
         
        file_name = cStringIO.StringIO(urllib.urlopen(self.URL).read())
        curr_img = Image.open(file_name)
        curr_img = curr_img.convert('RGB')
        width,height = curr_img.size
        
        self.imgsize = width*height
        
        colors_collect = curr_img.getcolors(self.imgsize)
        
        temp_check = colors_collect[0] #to catch files that return an integer instead of a list of RGB values
        if not isinstance(temp_check[1],int):  
            self.color_percents = measure_percents(colors_collect,self.imgsize)
        else:
            self.color_percents = None
        
    def get_URL(self):
        return self.URL
        
    def get_colors(self):
        return self.color_percents
    
    def get_size(self):
        return self.imgsize
    
    
#Converts RGB to YUV coordinates.  
def rgb_yuv(rgb):
    R,G,B = rgb[0],rgb[1],rgb[2]
    Y = (R*.299000) + (G*.587000) + (B*.114000)
    U = (R*-.168736) +(G*-.331264) + (B*.500000) + 128
    V = (R*.500000) + (G*-.418688) + (B*-.081312) + 128
    return (Y,U,V)

#Calculates Euclidean distance between two points
def euc_dist(p1,p2):
   return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2)+((p1[2]-p2[2])**2))

#Returns the closest common color approximate for a given specific RGB color
def approx_color(rgb):
    point1 = rgb_yuv((rgb[0],rgb[1],rgb[2])) 
    smallest = 443.405007 # Euclidean distance between (0,0,0) and (256,256,256)
    return_color = None 
    
    for curr_col in colors:
        temp_dist = euc_dist(point1,colors[curr_col]) #between two points in YUV color space
        if temp_dist<smallest:
            smallest = temp_dist
            return_color = curr_col  
    return return_color        

#Returns a list of common colors and the matching percentage they take up of the image
def measure_percents(colors_collect,imgsize):
 
    color_distr = {}
    for color in colors:
        color_distr[color] = 0
    for entry in colors_collect:
        color_distr[approx_color(entry[1])] += entry[0]
            
    color_list = []
    for i in color_distr:
        percentage = (100*((1.0*color_distr[i])/(imgsize)))
        color_list = color_list + [[i,percentage]]
    return color_list
