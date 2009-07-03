from django.conf import settings
from troggle.core.models import LogbookEntry
import random, re, logging

def weighted_choice(lst):
	n = random.uniform(0,1)
	for item, weight in lst:
		if n < weight:
			break
		n = n - weight
	return item

def randomLogbookSentence():
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
        logging.info(unicode(instance)+u' was just added to the database for the first time. \n')
    
    if not created and instance.new_since_parsing:
        logging.info(unicode(instance)+" has been modified using Troggle, so the current script left it as is. \n")

    if not created and not instance.new_since_parsing:
        logging.info(unicode(instance)+" existed in the database unchanged since last parse. It was overwritten by the current script. \n")
    return (instance, created)

def render_with_context(req, *args, **kwargs):
    """this is the snippet from http://www.djangosnippets.org/snippets/3/
    
    Django uses Context, not RequestContext when you call render_to_response. We always want to use RequestContext, so that django adds the context from settings.TEMPLATE_CONTEXT_PROCESSORS. This way we automatically get necessary settings variables passed to each template. So we use a custom method, render_response instead of render_to_response. Hopefully future Django releases will make this unnecessary."""

    from django.shortcuts import render_to_response
    from django.template import RequestContext
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)