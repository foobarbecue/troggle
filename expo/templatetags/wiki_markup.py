from django import template
from django.utils.html import conditional_escape
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import re

register = template.Library()

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
    if autoescape:
        value = conditional_escape(value)
    #deescape doubly escaped characters
    value = re.sub("&amp;(.*?);", r"&\1;", value, re.DOTALL)
    #italics and bold
    value = re.sub("&#39;&#39;&#39;&#39;([^']+)&#39;&#39;&#39;&#39;", r"<b><i>\1</i></b>", value, re.DOTALL)
    value = re.sub("&#39;&#39;&#39;([^']+)&#39;&#39;&#39;", r"<b>\1</b>", value, re.DOTALL)
    value = re.sub("&#39;&#39;([^']+)&#39;&#39;", r"<i>\1</i>", value, re.DOTALL)
    #Make lists from lines starting with lists of [stars and hashes]
    listdepth = []
    outValue = ""
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
