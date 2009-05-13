import troggle.settings as settings
import os

def urljoin(x, y): return x + "/" + y

def listdir(*path):
    try:
        l = ""
        root = os.path.join(settings.FILES, *path)
        for p in os.listdir(root):
            if os.path.isdir(os.path.join(root, p)):
                l += p + "/\n"
            elif os.path.isfile(os.path.join(root, p)):
                l += p + "\n"
            #Ignore non-files and non-directories
        return l
    except:
        return urllib.urlopen(settings.FILES + "listdir/" + reduce(urljoin, path))

def readFile(*path):
    try:
        f = open(os.path.join(settings.FILES, *path))
    except:
        f = urllib.urlopen(settings.FILES + "download/" + reduce(urljoin, path))
    return f.read()