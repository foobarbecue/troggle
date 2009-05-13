import troggle.settings as settings
import os
import urllib

def urljoin(x, y): return x + "/" + y

def listdir(*path):
    try:
        strippedpath = [p for p in path if p]
        root = os.path.join(settings.FILES, *strippedpath )
        l = ""
        #l = root + "\n"
        #isdir = os.path.isdir(root)
        #l += str(isdir) + "\n"
        for p in os.listdir(root):
            if os.path.isdir(os.path.join(root, p)):
                l += p + "/\n"
                
            elif os.path.isfile(os.path.join(root, p)):
                l += p + "\n"
            #Ignore non-files and non-directories
        return l
    except:
        if strippedpath:
            c = reduce(urljoin, strippedpath)
        else:
            c = ""
        print strippedpath, c
        return urllib.urlopen(settings.FILES + "listdir/" + c)


def readFile(*path):
    try:
        f = open(os.path.join(settings.FILES, *path))
    except:
        f = urllib.urlopen(settings.FILES + "download/" + reduce(urljoin, path))
    return f.read()