from django import template
from django.utils.html import conditional_escape
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.conf import settings
from core.models import QM, Photo, LogbookEntry, Cave
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
    """
    This is the tag which turns wiki syntax into html. It is intended for long pieces of wiki.
    Hence it splits the wiki into HTML paragraphs based on double line feeds.
    """
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
    This is the tag which turns wiki syntax into html. It is intended for short pieces of wiki.
    Hence it is not split the wiki into paragraphs using where it finds double line feeds.
    """
    if autoescape:
        value = conditional_escape(value)
    #deescape doubly escaped characters
    value = re.sub("&amp;(.*?);", r"&\1;", value, re.DOTALL)
    #italics and bold
    value = re.sub("&#39;&#39;&#39;&#39;([^']+)&#39;&#39;&#39;&#39;", r"<b><i>\1</i></b>", value, re.DOTALL)
    value = re.sub("&#39;b&#39;&#39;([^']+)&#39;&#39;&#39;", r"<b>\1</b>", value, re.DOTALL)
    value = re.sub("&#39;&#39;([^']+)&#39;&#39;", r"<i>\1</i>", value, re.DOTALL)

    #make headers
    def headerrepl(matchobj):
        number=len(matchobj.groups()[0])
        num=str(number)
        if number>1:
            return '<h'+num+'>'+matchobj.groups()[1]+'</h'+num+'>'
        else:
            print 'morethanone'
            return matchobj.group()
    value = re.sub(r"(?m)^(=+)([^=]+)(=+)$",headerrepl,value)
    
    #make qm links. this takes a little doing
    qmMatchPattern=settings.QM_PATTERN
    def qmrepl(matchobj):
        """
        A function for replacing wikicode qm links with html qm links.
        Given a matchobj matching a wikilink in the format
        [[QM:C204-1999-24]]
        If the QM does not exist, the function will return a link for creating it.
        """
        qmdict={'urlroot':url_root,'cave':matchobj.groups()[2],'year':matchobj.groups()[1],'number':matchobj.groups()[3]}
        try:
            qm=QM.objects.get(found_by__cave__kataster_number = qmdict['cave'],
                              found_by__date__year = qmdict['year'],
                              number = qmdict['number'])
            return r'<a href="%s" id="q%s">%s</a>' % (qm.get_absolute_url(), qm.code, unicode(qm))
        except QM.DoesNotExist: #bother aaron to make him clean up the below code - AC 
            try:
                placeholder=LogbookEntry.objects.get(date__year=qmdict['year'],cave__kataster_number=qmdict['cave'], title__icontains='placeholder')
            except LogbookEntry.DoesNotExist:
                placeholder=LogbookEntry(
                    date='01-01'+qmdict['year'],
                    cave=Cave.objects.get(kataster_number=qmdict['cave']),
                    title='placeholder'
                    )
            qm=QM(found_by = placeholder, number = qmdict['number'])
            return r'<a class="redtext" href="%s" id="q%s">%s</a>' % (qm.get_absolute_url(), qm.code, unicode(qm))

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

    #make cave links
    value = re.sub("\[\[\s*cave:([^\s]+)\s*\s*\]\]", r'<a href="%s/cave/\1/">\1</a>' % url_root, value, re.DOTALL)
    #make people links
    value = re.sub("\[\[\s*person:(.+)\|(.+)\]\]",r'<a href="%s/person/\1/">\2</a>' % url_root, value, re.DOTALL)
    #make subcave links
    value = re.sub("\[\[\s*subcave:(.+)\|(.+)\]\]",r'<a href="%s/subcave/\1/">\2</a>' % url_root, value, re.DOTALL)
    #make cavedescription links
    value = re.sub("\[\[\s*cavedescription:(.+)\|(.+)\]\]",r'<a href="%s/cavedescription/\2/">\2</a>' % url_root, value, re.DOTALL)


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
