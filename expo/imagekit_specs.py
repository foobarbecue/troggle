from imagekit.specs import ImageSpec
from imagekit import processors

class ResizeThumb(processors.Resize): 
    width = 100 
    height = 75 
    crop = True

class ResizeDisplay(processors.Resize):
    width = 600 
    
class EnhanceThumb(processors.Adjustment): 
    contrast = 1.2 
    sharpness = 1.1 

class Thumbnail(ImageSpec): 
    access_as = 'thumbnail_image' 
    pre_cache = True 
    processors = [ResizeThumb, EnhanceThumb] 

class Display(ImageSpec):
    increment_count = True
    processors = [ResizeDisplay]
