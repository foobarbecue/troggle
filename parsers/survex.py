import settings
import expo.models as models
import re
import os

re_include_extension = re.compile(r"^\s*\*include\s+([^\s]*).svx$", re.IGNORECASE)
re_include_no_extension = re.compile(r"^\s*\*include\s+([^\s]*)$", re.IGNORECASE)
re_begin = re.compile(r"^\s*\*begin\s+(.*?)\s*$", re.IGNORECASE)
re_end = re.compile(r"^\s*\*end\s+(.*?)\s*$", re.IGNORECASE)
re_date = re.compile(r"^\s*\*date\s+(.*?)\s*$", re.IGNORECASE)

def fileIterator(directory, filename):
    survex_file = os.path.join(directory, filename + ".svx")
    try:
        f = open(os.path.join(settings.SURVEX_DATA, survex_file), "rb")
    except:
        f = open(os.path.join(settings.SURVEX_DATA, survex_file).lower(), "rb")
    char = 0
    for line in f.readlines():
        line = unicode(line, "latin1")
        include_extension = re_include_extension.match(line)
        include_no_extension = re_include_no_extension.match(line)
        def a(include):
            link = re.split(r"/|\\", include)
            return fileIterator(os.path.join(directory, *link[:-1]), link[-1])
        if include_extension:
            for sf, c, l in a(include_extension.groups()[0]):
                yield sf, c, l
        elif include_no_extension:
            for sf, c, l in a(include_no_extension.groups()[0]):
                yield sf, c, l
        else:
            yield survex_file, char, line
        char = char + len(line)

def make_model(name, parent, iter_lines, sf, c, l):
    if parent:
        m = models.SurvexBlock(name = name, parent = parent, begin_file = sf, begin_char = c, text = l)
    else:
        m = models.SurvexBlock(name = name, begin_file = sf, begin_char = c, text = l)
    m.save()
    for survex_file, count, line in iter_lines:
      begin = re_begin.match(line.split(";")[0])
      end = re_end.match(line.split(";")[0])
      date = re_date.match(line.split(";")[0])
      if begin:
          make_model(begin.groups()[0], m, iter_lines, survex_file, count, line)
      elif end:
          m.text = m.text + line
          m.end_file = survex_file
          m.end_char = count
          m.save()
          assert (end.groups()[0]).lower() == (name).lower()
          return None
      elif date:
          #print date.groups()[0]
          m.text = m.text + line
      else:
          m.text = m.text + line
    m.text = m.text + line
    m.end_file = survex_file
    m.end_char = count
    m.save()


filename = "all"
make_model("", None, fileIterator("", filename), filename, 0, "")
