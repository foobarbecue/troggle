from django import template
from django.utils.html import conditional_escape
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import re

register = template.Library()

# seems to add extra lines between the commented lines, which isn't so great.
regexes = []
regexes.append((re.compile(r"(;.*)$", re.IGNORECASE|re.MULTILINE),
               r'<span class = "comment">\1</span>\n'))
regexes.append((re.compile(r"^(\s*)(\*include)(\s+)([^\s]*)(.svx)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3<a href="\4.index">\4\5</a>'))
regexes.append((re.compile(r"^(\s*)(\*include)(\s+)([^\s]*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3<a href="\4.index">\4</a>'))
regexes.append((re.compile(r"^(\s*)(\*team\s+(?:notes|tape|insts|pics))(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*(?:begin|end|copyright|date|entrance|equate|export|fix|prefix|require|SOLVE|title|truncate))(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*calibrate\s+(?:TAPE|COMPASS|CLINO|COUNTER|DEPTH|DECLINATION|X|Y|Z)+)(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*data\s+(?:DEFAULT|NORMAL|DIVING|CARTESIAN|TOPOFIL|CYLPOLAR|NOSURVEY|passage)(?:\s+station|\s+from|\s+to|\s+FROMDEPTH|\s+TODEPTH|\s+DEPTHCHANGE|\s+newline|\s+direction|\s+tape|\s+compass|\s+clino|\s+northing|\s+easting|\s+altitude|\s+length|\s+bearing|\s+gradient|\s+ignoreall|\sleft|\sright|\sup|\sdown)*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>'))
regexes.append((re.compile(r"^(\s*)(\*default\s+(?:CALIBRATE|DATA|UNITS)+)(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*flags\s+(?:DUPLICATE|SPLAY|SURFACE|not DUPLICATE|not SPLAY|not SURFACE))(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*infer\s+(?:plumbs|equates|exports))(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*instrument\s+(?:compass|clino|tape))(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*instrument\s+(?:compass|clino|tape))(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*sd\s+(?:TAPE|COMPASS|CLINO|COUNTER|DEPTH|DECLINATION|DX|DY|DZ))(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*set\s+(?:BLANK|COMMENT|DECIMAL|EOL|KEYWORD|MINUS|NAMES|OMIT|PLUS|ROOT|SEPARATOR))(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(\s*)(\*units\s+(?:TAPE|LENGTH|COMPASS|BEARING|CLINO|GRADIENT|COUNTER|DEPTH|DECLINATION|X|Y|Z))(\s+)(.*)$", re.IGNORECASE|re.MULTILINE),
                r'\1<span class = "command">\2</span>\3\4'))
regexes.append((re.compile(r"^(.*)$", re.IGNORECASE|re.MULTILINE),
                r'<div>\1&nbsp;</div>\n'))

@register.filter()
@stringfilter
def survex_to_html(value, autoescape=None):
    if autoescape:
        value = conditional_escape(value)
    for regex, sub in regexes:
        print sub
        value = regex.sub(sub, value)
    return mark_safe(value)