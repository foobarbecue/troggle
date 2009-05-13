import settings
import expo.models as models

from troggle.parsers.people import GetPersonExpeditionNameLookup

import re
import os

roles = {"Insts": "Insts",
         "insts": "Insts",
         "Instruments": "Insts",
         "instruments": "Insts",
         "Inst": "Insts",
         "inst": "Insts",
         "dog": "Other",
         "Dog": "Other",
         "other": "Other",
         "Other": "Other",
         "Notes": "Notes",
         "notes": "notes",
         "pics": "Pics",
         "Pics": "Pics",
         "Tape": "Tape",
         "tape": "Tape"}

re_include_extension = re.compile(r"^\s*\*include\s+([^\s]*).svx$", re.IGNORECASE)
re_include_no_extension = re.compile(r"^\s*\*include\s+([^\s]*)$", re.IGNORECASE)
flags = {"begin": re.compile(r"^\s*\*begin\s+(.*?)\s*$", re.IGNORECASE),
         "end": re.compile(r"^\s*\*end\s+(.*?)\s*$", re.IGNORECASE),
         "date": re.compile(r"^\s*\*date\s+(.*?)\s*$", re.IGNORECASE),
         "team": re.compile(r"^\s*\*team\s+(.*?)\s*$", re.IGNORECASE)}

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
    m = models.SurvexBlock(name = name, begin_file = sf, begin_char = c, text = l)
    m.survexpath = m.name
    if parent:
        m.parent = parent
        m.survexpath = m.parent.survexpath + "." + m.name
    m.save()

    # horrible local function
    def saveEnd(survex_file, count):
          if m.start_year and team:
              try:
                  exp = models.Expedition.objects.get(year = str(m.start_year))
                  for file_, (role, names) in team:
                      if names.strip("\t").strip(" ") == "both" or names.strip("\t").strip(" ") == "Both":
                          names = reduce(lambda x, y: x + u" & " + y,
                                         [names for file_, (role, names) in team
                                                if names.strip("\t").strip(" ") != "both"
                                                   and names.strip("\t").strip(" ") != "Both"])
                      for name in re.split("&|/|\+|,|;", names):
                          sname = name.strip(". ").lower()
                          try:
                              personexpedition = GetPersonExpeditionNameLookup(exp).get(sname)
                              if personexpedition:
                                  models.PersonRole(personexpedition = personexpedition,
                                                person = personexpedition.person,
                                                survex_block = m,
                                                role = models.Role.objects.get(name = roles[role])).save()
                              else:
                                  print "no person", exp, sname, role
                          except AttributeError:
                              print ("Person not found: " + name + " in " + file_ + "  " + role).encode('ascii', 'xmlcharrefreplace')
              except AssertionError, inst:
                  print (unicode(inst) + ": " + unicode(file_year[0])).encode('ascii', 'xmlcharrefreplace')
              #except models.Expedition.DoesNotExist:
              #    print "Expo"+str(file_year[1]).encode('ascii', 'xmlcharrefreplace')

          m.end_file = survex_file
          m.end_char = count
          
          if m.start_day:
              m.date = "%04d-%02d-%02d" % (int(m.start_year), int(m.start_month), int(m.start_day))
          
          m.save()
    
    team = []
    file_year = None
    for survex_file, count, line in iter_lines:
      #Dictionary compreshension
      res = dict([(key, regex.match(line.split(";")[0])) for key, regex in flags.iteritems()])
      if res["begin"]:
          make_model(res["begin"].groups()[0], m, iter_lines, survex_file, count, line)
      else:
          m.text = m.text + line
      if res["end"]:
          saveEnd(survex_file, count)
          assert (res["end"].groups()[0]).lower() == (name).lower()
          return None
      elif res["date"]:
          datere = re.match("(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:-(\d+))?(?:\.(\d+))?(?:\.(\d+))?",
                            res["date"].groups()[0])
          if datere is not None:
              startYear, startMonth, startDay, endYear, endMonth, endDay = datere.groups()
              m.start_year = startYear
              m.start_month = startMonth
              m.start_day = startDay
              m.end_year = endYear
              m.end_month = endMonth
              m.end_day = endDay
          file_year = survex_file, startYear
      elif res["team"]:
          h = re.match("((?:[Ii]nst(?:s|ruments)?)|(?:[Pp]ics)|(?:[Tt]ape)|(?:[Nn]otes)|(?:[Oo]ther))\s*(.*)",
                       res["team"].groups()[0])
          if h:
              team.append((survex_file, h.groups()))
          else:
              print ("Role not found: " +  line + " in: " + sf).encode('ascii', 'xmlcharrefreplace')
    m.text = m.text + line
    saveEnd(survex_file, count)


#def LoadSurvexBlocks():
#    survex_file = os.path.join(directory, filename + ".svx")
#    f = open(os.path.join(settings.SURVEX_DATA, survex_file), "rb")


def LoadAllSurvexBlocks():
    models.Role.objects.all().delete()
    models.SurvexBlock.objects.all().delete()
    for role in ["Insts", "Notes", "Pics", "Tape", "Other"]:
        models.Role(name = role).save()
    filename = "all"
    make_model("all", None, fileIterator("", filename), filename, 0, "")


