from imagekit.specs import ImageSpec
from imagekit import processors

class ResizeThumb(processors.Resize): 
    width = 100 
    crop = False

class ResizeDisplay(processors.Resize):
    width = 600 
    
#class EnhanceThumb(processors.Adjustment): 
    #contrast = 1.2
    #sharpness = 2

class Thumbnail(ImageSpec): 
    access_as = 'thumbnail_image' 
    pre_cache = True 
    processors = [ResizeThumb] 

class Display(ImageSpec):
    increment_count = True
    processors = [ResizeDisplay]
