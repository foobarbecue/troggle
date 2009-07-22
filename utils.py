from django.conf import settings
import random, re, logging
from core.models import CaveDescription

def weighted_choice(lst):
	n = random.uniform(0,1)
	for item, weight in lst:
		if n < weight:
			break
		n = n - weight
	return item

def randomLogbookSentence():
    from troggle.core.models import LogbookEntry
    randSent={}

    # needs to handle empty logbooks without crashing

    #Choose a random logbook entry
    randSent['entry']=LogbookEntry.objects.order_by('?')[0]

    #Choose again if there are no sentances (this happens if it is a placeholder entry)
    while len(re.findall('[A-Z].*?\.',randSent['entry'].text))==0:
        randSent['entry']=LogbookEntry.objects.order_by('?')[0]
    
    #Choose a random sentence from that entry. Store the sentence as randSent['sentence'], and the number of that sentence in the entry as randSent['number']
    sentenceList=re.findall('[A-Z].*?\.',randSent['entry'].text)
    randSent['number']=random.randrange(0,len(sentenceList))
    randSent['sentence']=sentenceList[randSent['number']]
           
    return randSent


def save_carefully(objectType, lookupAttribs={}, nonLookupAttribs={}):
    """Looks up instance using lookupAttribs and carries out the following:
            -if instance does not exist in DB: add instance to DB, return (new instance, True)
            -if instance exists in DB and was modified using Troggle: do nothing, return (existing instance, False)
            -if instance exists in DB and was not modified using Troggle: overwrite instance, return (instance, False)
            
        The checking is accomplished using Django's get_or_create and the new_since_parsing boolean field
        defined in core.models.TroggleModel.
    
    """

    instance, created=objectType.objects.get_or_create(defaults=nonLookupAttribs, **lookupAttribs)

    if not created and not instance.new_since_parsing:
        for k, v in nonLookupAttribs.items(): #overwrite the existing attributes from the logbook text (except date and title)
            setattr(instance, k, v)
        instance.save()
    
    if created:
        logging.info(str(instance) + ' was just added to the database for the first time. \n')
    
    if not created and instance.new_since_parsing:
        logging.info(str(instance) + " has been modified using Troggle, so the current script left it as is. \n")

    if not created and not instance.new_since_parsing:
        logging.info(str(instance) + " existed in the database unchanged since last parse. It was overwritten by the current script. \n")
    return (instance, created)

def render_with_context(req, *args, **kwargs):
    """this is the snippet from http://www.djangosnippets.org/snippets/3/

    Django uses Context, not RequestContext when you call render_to_response.
    We always want to use RequestContext, so that django adds the context from
    settings.TEMPLATE_CONTEXT_PROCESSORS. This way we automatically get
    necessary settings variables passed to each template. So we use a custom
    method, render_response instead of render_to_response. Hopefully future
    Django releases will make this unnecessary."""

    from django.shortcuts import render_to_response
    from django.template import RequestContext
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)
    
re_body = re.compile(r"\<body[^>]*\>(.*)\</body\>", re.DOTALL)
re_title = re.compile(r"\<title[^>]*\>(.*)\</title\>", re.DOTALL)

def get_html_body(text):
    return get_single_match(re_body, text)

def get_html_title(text):
    return get_single_match(re_title, text)

def get_single_match(regex, text):
    match = regex.search(text)

    if match:
        return match.groups()[0]
    else:
        return None

def href_to_wikilinks(matchobj):
    """
    Given an html link, checks for possible valid wikilinks.
    
    Returns the first valid wikilink. Valid means the target
    object actually exists.
    """
    res=CaveDescription.objects.filter(long_name__icontains=matchobj.groupdict()['text'])
    if res[0]:
        return r'[[cavedescription:'+res[0].short_name+'|'+res[0].long_name+']]'
    else:
        return matchobj.group()
    #except:
        #print 'fail'
    

re_subs = [(re.compile(r"\<b[^>]*\>(.*?)\</b\>", re.DOTALL), r"'''\1'''"),
           (re.compile(r"\<i\>(.*?)\</i\>", re.DOTALL), r"''\1''"),
           (re.compile(r"\<h1[^>]*\>(.*?)\</h1\>", re.DOTALL), r"=\1="),
           (re.compile(r"\<h2[^>]*\>(.*?)\</h2\>", re.DOTALL), r"==\1=="),
           (re.compile(r"\<h3[^>]*\>(.*?)\</h3\>", re.DOTALL), r"===\1==="),
           (re.compile(r"\<h4[^>]*\>(.*?)\</h4\>", re.DOTALL), r"====\1===="),
           (re.compile(r"\<h5[^>]*\>(.*?)\</h5\>", re.DOTALL), r"=====\1====="),
           (re.compile(r"\<h6[^>]*\>(.*?)\</h6\>", re.DOTALL), r"======\1======"),
           (re.compile(r'(<a href="?(?P<target>.*)"?>)?<img class="?(?P<class>\w*)"? src="?t/?(?P<source>[\w/\.]*)"?(?P<rest>></img>|\s/>(</a>)?)', re.DOTALL),r'[[display:\g<class> photo:\g<source>]]'), #
           (re.compile(r"\<a\s+id=['\"]([^'\"]*)['\"]\s*\>(.*?)\</a\>", re.DOTALL), r"[[subcave:\1|\2]]"), #assumes that all links with id attributes are subcaves. Not great.
           #interpage link needed
           (re.compile(r"\<a\s+href=['\"]#([^'\"]*)['\"]\s*\>(.*?)\</a\>", re.DOTALL), r"[[cavedescription:\1|\2]]"), #assumes that all links with target ids are cave descriptions. Not great.
           (re.compile(r"\[\<a\s+href=['\"][^'\"]*['\"]\s+id=['\"][^'\"]*['\"]\s*\>([^\s]*).*?\</a\>\]", re.DOTALL), r"[[qm:\1]]"),
           (re.compile(r'<a\shref="?(?P<target>.*)"?>(?P<text>.*)</a>'),href_to_wikilinks),
           
           ]

def html_to_wiki(text, codec = "utf-8"):
    if type(text) == str:
        text = unicode(text, codec)
    text = re.sub("</p>", r"", text)
    text = re.sub("<p>$", r"", text)
    text = re.sub("<p>", r"\n\n", text)
    out = ""
    lists = ""
    #lists
    while text:
        mstar = re.match("^(.*?)<ul[^>]*>\s*<li[^>]*>(.*?)</li>(.*)$", text, re.DOTALL)
        munstar = re.match("^(\s*)</ul>(.*)$", text, re.DOTALL)
        mhash = re.match("^(.*?)<ol[^>]*>\s*<li[^>]*>(.*?)</li>(.*)$", text, re.DOTALL)
        munhash = re.match("^(\s*)</ol>(.*)$", text, re.DOTALL)
        mitem = re.match("^(\s*)<li[^>]*>(.*?)</li>(.*)$", text, re.DOTALL)
        ms = [len(m.groups()[0]) for m in [mstar, munstar, mhash, munhash, mitem] if m]
        def min_(i, l):
            try:
                v = i.groups()[0]
                l.remove(len(v))
                return len(v) < min(l, 1000000000)
            except:
                return False
        if min_(mstar, ms):
            lists += "*"
            pre, val, post = mstar.groups()
            out += pre + "\n" + lists + " " + val
            text = post
        elif min_(mhash, ms):
            lists += "#"
            pre, val, post = mhash.groups()
            out += pre + "\n" + lists + " " + val
            text = post
        elif min_(mitem, ms):
            pre, val, post = mitem.groups()
            out += "\n" + lists + " " + val
            text = post
        elif min_(munstar, ms):
            lists = lists[:-1]
            text = munstar.groups()[1]
        elif min_(munhash, ms):
            lists.pop()
            text = munhash.groups()[1]
        else:
            out += text
            text = ""
    #substitutions
    for regex, repl in re_subs:
        out = regex.sub(repl, out)
    return out


