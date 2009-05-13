import troggle.settings as settings
from django import forms
from expo.models import LogbookEntry
import random
import re

def weighted_choice(lst):
	n = random.uniform(0,1)
	for item, weight in lst:
		if n < weight:
			break
		n = n - weight
	return item

def randomLogbookSentence():
    #Choose a random logbook entry
    randSent={}
    randSent['entry']=LogbookEntry.objects.order_by('?')[0]
    
    #Choose a random sentence from that entry. Store the sentence as randSent['sentence'], and the number of that sentence in the entry as randSent['number']
    sentenceList=re.findall('[A-Z].*?\.',randSent['entry'].text)
    randSent['number']=random.randrange(0,len(sentenceList))
    randSent['sentence']=sentenceList[randSent['number']]
    return randSent