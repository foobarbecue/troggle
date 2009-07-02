from django import template
from django.utils.html import conditional_escape
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.conf import settings
from core.models import QM, Photo
import re, urlparse

register = template.Library()
if settings.URL_ROOT.endswith('/'):
    url_root=settings.URL_ROOT[:-1]
                
def wiki_list(line, listdepth):
        l = ""
        for d in listdepth:
            l += d
        mstar = re.match(l + "\*(.*)", line)
        if mstar:
            listdepth.append("\*")
            return ("<ul>\n" + " " * len(listdepth) + "<li>%s</li>\n" % mstar.groups()[0], listdepth)
        mhash = re.match(l + "#(.*)", line)
        if mhash:
            listdepth.append("#")
            return ("<ol>\n" + " " * len(listdepth) + "<li>%s</li>\n" % mhash.groups()[0], listdepth)
        mflat = re.match(l + "(.*)", line)
        if mflat and listdepth:
            return (" " * len(listdepth) + "<li>%s</li>\n" % mflat.groups()[0], listdepth)
        if listdepth:
            prev = listdepth.pop()
            if prev == "\*":
                t, l = wiki_list(line, listdepth)
                return ("</ul>\n" + t, l)
            if prev == "#":
                t, l = wiki_list(line, listdepth)
                return ("</ol>\n" + t, l)
        return (line, listdepth)

@register.filter()
@stringfilter
def wiki_to_html(value, autoescape=None):
    #find paragraphs
    outValue = ""
    for paragraph in re.split("\n\s*?\n", value, re.DOTALL):
        outValue += "<p>"
        outValue += wiki_to_html_short(paragraph, autoescape)
        outValue += "</p>\n"
    return mark_safe(outValue)

@register.filter()
@stringfilter
def wiki_to_html_short(value, autoescape=None):
    """
    This is the tag which turns wiki syntax into html. Aaron wonders
    why it is called "short." It is long, and it operates on long things.
    It even has a long name itself.
    """
    if autoescape:
        value = conditional_escape(value)
    #deescape doubly escaped characters
    value = re.sub("&amp;(.*?);", r"&\1;", value, re.DOTALL)
    #italics and bold
    value = re.sub("&#39;&#39;&#39;&#39;([^']+)&#39;&#39;&#39;&#39;", r"<b><i>\1</i></b>", value, re.DOTALL)
    value = re.sub("&#39;&#39;&#39;([^']+)&#39;&#39;&#39;", r"<b>\1</b>", value, re.DOTALL)
    value = re.sub("&#39;&#39;([^']+)&#39;&#39;", r"<i>\1</i>", value, re.DOTALL)
    #make cave links
    value = re.sub("\[\[\s*cave:([^\s]+)\s*\s*\]\]", r'<a href="%s/cave/\1/">\1</a>' % url_root, value, re.DOTALL)
    #make people links
    value = re.sub("\[\[\s*person:(.+)\]\]",r'<a href="%s/person/\1/">\1</a>' % url_root, value, re.DOTALL)
    
    #make qm links. this takes a little doing
    qmMatchPattern="\[\[\s*cave:([^\s]+)\s*\s*\QM:(\d*)-(\d*)([ABCDX]?)\]\]"
    def qmrepl(matchobj):
        """
        A function for replacing wikicode qm links with html qm links.
        Given a matchobj matching a wikilink in the format 
        [[cave:204 QM:1999-24C]] where the grade (C) is optional.
        If the QM does not exist, the function will return a link for creating it.
        """
        # if there are four matched groups, the fourth one should be the QM grade 
        if len(matchobj.groups())==4:
            grade=matchobj.groups()[3]
        else:
            grade=''
        qmdict={'urlroot':url_root,'cave':matchobj.groups()[0],'year':matchobj.groups()[1],'number':matchobj.groups()[2],'grade':grade}
        try:
            qm=QM.objects.get(found_by__cave__kataster_number=qmdict['cave'],found_by__date__year=qmdict['year'], number=qmdict['number'])
            res=r'<a href=' + str(qm.get_absolute_url()) +'>' + str(qm) + '</a>'
        except QM.DoesNotExist:
            res = r'<a class="redtext" href="%(urlroot)s/cave/%(cave)s/%(year)s-%(number)s%(grade)s">%(cave)s:%(year)s-%(number)s%(grade)s</a>' % qmdict
        return res 
    value = re.sub(qmMatchPattern,qmrepl, value, re.DOTALL)
    
    #make photo links for [[photo:filename]] or [[photo:filename linktext]], and
    #insert photos for [[display:left photo:filename]]
    photoLinkPattern="\[\[\s*photo:(?P<photoName>[^\s]+)\s*(?P<linkText>.*)\]\]"
    photoSrcPattern="\[\[\s*display:(?P<style>[^\s]+) photo:(?P<photoName>[^\s]+)\s*\]\]"
    def photoLinkRepl(matchobj):
        matchdict=matchobj.groupdict()
        try:
            linkText=matchdict['linkText']
        except KeyError:
            linkText=None
        
        try:
            photo=Photo.objects.get(file=matchdict['photoName'])
            if not linkText:
                linkText=str(photo)
            res=r'<a href=' + photo.get_admin_url() +'>' + linkText + '</a>'
        except Photo.DoesNotExist:
            res = r'<a class="redtext" href="">make new photo</a>'
        return res

    def photoSrcRepl(matchobj):
        matchdict=matchobj.groupdict()
        style=matchdict['style']
        try:
            photo=Photo.objects.get(file=matchdict['photoName'])
            res=r'<a href='+photo.file.url+'><img src=' + photo.thumbnail_image.url +' class='+style+' /></a>'
        except Photo.DoesNotExist:
            res = r'<a class="redtext" href="">make new photo</a>'
        return res
    value = re.sub(photoLinkPattern,photoLinkRepl, value, re.DOTALL)
    value = re.sub(photoSrcPattern,photoSrcRepl, value, re.DOTALL)
    
    #Make lists from lines starting with lists of [stars and hashes]
    outValue = ""
    listdepth = []
    for line in value.split("\n"):
        t, listdepth = wiki_list(line, listdepth)
        outValue += t
    for item in listdepth:
        if item == "\*":
            outValue += "</ul>\n"
        elif item == "#":
            outValue += "</ol>\n"
    return mark_safe(outValue)

wiki_to_html.needs_autoescape = True