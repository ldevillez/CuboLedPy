
def writeVal(f ,data, Ops, shouldFinish):
  dt = int(data)
  if Ops['OutputType'] == 'txt':
    f.write(str(dt))
    if not shouldFinish:
      f.write(Ops['Separator'])
  elif Ops['OutputType'] == 'header':
    f.write(str(dt))
    if not shouldFinish:
      f.write(", ")
  else:
    #protection
    sys.exit("OUTPUT TYPE UNKNOWN")

def writeHeader(f, Ops):
  if Ops['OutputType'] == 'txt':
    return
  elif Ops['OutputType'] == 'header':
    f.write("const int nbStep = " + str(int(Ops['TimeLength']/Ops['Delay'])) + ";\n")
    f.write("const int delayStep = " + str(Ops['Delay']) + ";\n")
    f.write("const int nbLedSegment = " + str(Ops['LedsBySegment']) + ";\n")
    f.write("const int nbSegment = " + str(Ops['nbSegment']) + ";\n\n")
    f.write("const int segments[nbSegment][nbLedSegment][nbStep * 3] = {\n")
  else:
    #protection
    sys.exit("OUTPUT TYPE UNKNOWN")

def writeLedStart(f,Ops):
  if Ops['OutputType'] == 'txt':
    return
  elif Ops['OutputType'] == 'header':
    f.write("\t\t{")
  else:
    #protection
    sys.exit("OUTPUT TYPE UNKNOWN")

def writeLedEnd(f,Ops,shouldFinish):
  if Ops['OutputType'] == 'txt':
    f.write("\n")
  elif Ops['OutputType'] == 'header':
    f.write("},\n")
  else:
    #protection
    sys.exit("OUTPUT TYPE UNKNOWN")


def writeSegStart(f,Ops):
  if Ops['OutputType'] == 'txt':
    return
  elif Ops['OutputType'] == 'header':
    f.write("\t{\n")
  else:
    #protection
    sys.exit("OUTPUT TYPE UNKNOWN")
def writeSegEnd(f,Ops,shouldFinish):
  if Ops['OutputType'] == 'txt':
    return
  elif Ops['OutputType'] == 'header':
    f.write("\t},\n")
    if shouldFinish:
      f.write("};")
  else:
    #protection
    sys.exit("OUTPUT TYPE UNKNOWN")