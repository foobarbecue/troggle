import settings
import expo.models as models
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
    if parent:
        m = models.SurvexBlock(name = name, parent = parent, begin_file = sf, begin_char = c, text = l)
    else:
        m = models.SurvexBlock(name = name, begin_file = sf, begin_char = c, text = l)
    m.save()

    def saveEnd(survex_file, count):
          if m.start_year and team:
              try:
                  exp = models.Expedition.objects.get(year = str(file_year[1]))
                  for file_, (role, names) in team:
                      if names.strip("\t").strip(" ") == "both" or names.strip("\t").strip(" ") == "Both":
                          names = reduce(lambda x, y: x + u" & " + y,
                                         [names for file_, (role, names) in team
                                                if names.strip("\t").strip(" ") != "both"
                                                   and names.strip("\t").strip(" ") != "Both"])
                      for name in re.split("&|/|\+|,|;", names):
                          try:
                              models.PersonRole(personexpedition = exp.GetPersonExpedition(name.strip(" ")),
                                                person = exp.GetPersonExpedition(name.strip(" ")).person,
                                                survex_block = m,
                                                role = models.Role.objects.get(name = roles[role])).save()
                          except AttributeError:
                              print ("Person not found: " + name + " in " + file_).encode('ascii', 'xmlcharrefreplace')
              except AssertionError, inst:
                  print (unicode(inst) + ": " + unicode(file_year[0])).encode('ascii', 'xmlcharrefreplace')
              except models.Expedition.DoesNotExist:
                  print "Expo"+str(file_year[1]).encode('ascii', 'xmlcharrefreplace')

          m.end_file = survex_file
          m.end_char = count
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


for role in ["Insts", "Notes", "Pics", "Tape", "Other"]:
    models.Role(name = role).save()

filename = "all"
make_model("", None, fileIterator("", filename), filename, 0, "")
