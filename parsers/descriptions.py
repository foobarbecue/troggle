from django.conf import settings
import core.models as models
import os
from utils import html_to_wiki, get_html_body, get_html_title

pages = [(["smkridge", "204", "ariston-rigging.html"], "ariston-rigging"),
         (["smkridge", "204", "ariston.html"], "ariston"),
         (["smkridge", "204", "bivvy.html"], "bivvy"),
         (["smkridge", "204", "bridge.html"], "bridge"),
         (["smkridge", "204", "entrance-rigging.html"], "entrance-rigging"),
         (["smkridge", "204", "entrance.html"], "entrance"),
         (["smkridge", "204", "midlevel.html"], "midlevel"),
         (["smkridge", "204", "millennium.html"], "millennium"),
         (["smkridge", "204", "nopain.html"], "nopain"),
         (["smkridge", "204", "razordance.html"], "razordance"),
         (["smkridge", "204", "rhino.html"], "rhino"),
         (["smkridge", "204", "sbview.html"], "sbview"),
         (["smkridge", "204", "subway.html"], "subway"),
         (["smkridge", "204", "swings.html"], "swings"),
         (["smkridge", "204", "treeumphant.html"], "treeumphant"),
         (["smkridge", "204", "uworld.html"], "uworld"), ]


def getDescriptions():
    """Creates objects in the database for each item in the list 'pages' . """
    for filelocation, name in pages:
        f = open(os.path.join(settings.EXPOWEB, *filelocation), "r")
        html = f.read()

        cd = models.CaveDescription(short_name = name,
                                    long_name = unicode(get_html_title(html), "latin1"),
                                    description = unicode(get_html_body(html), "latin1"))
        cd.save()

def parseDescriptions():
    """Turns the HTML in each cave description into wikicode"""
    for cd in models.CaveDescription.objects.all():
        cd.description = html_to_wiki(cd.description)

        cd.save()

def parseDescriptionsOnCaveObjects():
    for cave in models.Cave.objects.all():
        cave.underground_description=html_to_wiki(unicode(cave.underground_description))
        cave.save()