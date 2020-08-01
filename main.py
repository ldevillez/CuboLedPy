import json
import codecs
import sys

from utils import Linear, Quadratic
from fileHandler import writeVal, writeHeader, writeLedStart, writeLedEnd,writeSegStart, writeSegEnd


name = 'data.json'

data = {}

try:
  # We open the file
  with codecs.open(name,'r','utf-8') as json_file:
  # We load the JSON
    data = json.load(json_file)
except IOError:
  sys.exit('The file ' + name + ' is not found!')


print('Checking if everything is here...')

#Options required
opsToTry = [
  'nbSegment',
  'LedsBySegment',
  'TimeLength',
  'Delay',
  'Output',
  'OutputType'
]

Ops = data['Options']

for op in opsToTry:
  if op not in Ops:
    sys.exit('The options must have a key "' + op + '"')


# Check if the data are good
nbSeg = Ops['nbSegment']
if nbSeg != len(data["Segments"]):
  sys.exit('You requested ' + str(nbSeg) + " segments but we found " + str(data["Segments"]))

fileName = Ops['Output']
if Ops['OutputType'] == "txt":
  fileName += '.txt'
elif Ops['OutputType'] == "header":
  fileName += '.h'
else:
  sys.exit('The output type "' + Ops['OutputType'] + '" is unknown')


try:
  with open(fileName,'w+') as f:
    print('Ok ! Starting to work')
    writeHeader(f,Ops)

    N = Ops['LedsBySegment']
    for idxSeg, Seg in enumerate(data['Segments']):
      writeSegStart(f,Ops)
      for Led in range(N):
        writeLedStart(f,Ops)
        LastColor = [0, 0, 0]
        nbIter = 0
        for dataStep in Seg:
          Li = [0, 0, 0]
          Le = [0, 0, 0]
          # TODO add verication of parameter in each type of step
          # SPATIAL
          if dataStep['TypeSpatial'] == 'Linear':
            Li = Linear(dataStep['ColorTiSi'], dataStep['ColorTiSe'], Led, N)
            Le = Linear(dataStep['ColorTeSi'], dataStep['ColorTeSe'], Led, N)

          # TODO handle single led case
          elif dataStep['TypeSpatial'] == 'Quadratic':
            Li = Quadratic(dataStep['ColorTiSi'], dataStep['ColorTiSe'], Led, N)
            Le = Quadratic(dataStep['ColorTeSi'], dataStep['ColorTeSe'], Led, N)
          else:
            sys.exit('The spatial type "' + dataStep['TypeSpatial'] + '" is unknown')

          # TEMPORAL
          nbStep = int(dataStep['TimeLength'] / Ops['Delay'])
          for step in range(nbStep):
            shouldBreak = False
            if (nbIter+1) * Ops['Delay'] >= Ops['TimeLength']:
              shouldBreak = True

            if dataStep['TypeTemporal'] == 'Linear':
              LastColor = Linear(Li, Le, step, nbStep)
            elif dataStep['TypeTemporal'] == 'Quadratic':
              LastColor = Quadratic(Li, Le, step, nbStep)
            else:
              sys.exit('The temporal type "' + dataStep['TypeTemporal'] + '" is unknown')


            # EFFECT zone
            printColor = [0,0,0]
            if "Effect" in dataStep:
              Effect = dataStep['Effect']
              newStep = step / Effect['StepNumber']
              if Effect['Type'] == 'Rain':
                indiceLed = Led +1
                if Effect['Reverse']:
                  indiceLed = N+1-indiceLed
                if (newStep/ Effect['StepNumber'] + 1) % (N) == indiceLed:
                  for i in range(3):
                    printColor[i] = Effect['Color'][i]
                else:
                  for i in range(3):
                    printColor[i] = LastColor[i]
              elif Effect['Type'] == 'Rebound':
                indiceLed = Led +1
                if Effect['Reverse']:
                  indiceLed = N+1-indiceLed
                LedToShow = 1

                if newStep < N:
                  LedToShow = newStep +1
                elif (newStep - LedsBySegment) % 2*(N - 1) < N -1:
                  LedToShow = N - 1 -(newStep - LedsBySegment) % (N - 1)
                else: 
                  LedToShow = 2 + (newStep - LedsBySegment) % (N - 1)
                if LedToShow == indiceLed:
                  for i in range(3):
                    printColor[i] = Effect['Color'][i]
                else:
                  for i in range(3):
                    printColor[i] = LastColor[i]
              elif Effect['Type'] == 'Zigzag':
                val = newStep % 2
                if Effect['Reverse']:
                  val = 1 - val
                if (val == Led % 2):
                  for i in range(3):
                    printColor[i] = Effect['Color'][i]
                else:
                  for i in range(3):
                    printColor[i] = LastColor[i]
              elif Effect['Count']:
                iterStep = newStep % (N * (N + 1)/2)
                NLed = Led
                if Effect['Reverse']:
                  NLed = N - 1 - Led
                LedInv = N - NLed
        
                if iterStep >= (N * (N+1) - (N - LedInv) * (N - LedInv +1))/2:
                  for i in range(3):
                    printColor[i] = Effect['Color'][i]
                else:
                  offset = 0
                  toAdd = N
                  while offset + toAdd < iterStep:
                    offset += toAdd
                    N -= 1
                  if NLed +1 == iterStep - offset:
                    for i in range(3):
                      printColor[i] = Effect['Color'][i]
                  else:
                    for i in range(3):
                      printColor[i] = LastColor[i]
              elif Effect['Uncount']:
                iterStep = N * (N + 1)/2 - 1 -(newStep % (N * (N + 1)/2))
                NLed = Led
                if Effect['Reverse']:
                  NLed = N - 1 - Led
                LedInv = N - NLed
        
                if iterStep >= (N * (N+1) - (N - LedInv) * (N - LedInv +1))/2:
                  for i in range(3):
                    printColor[i] = Effect['Color'][i]
                else:
                  offset = 0
                  toAdd = N
                  while offset + toAdd < iterStep:
                    offset += toAdd
                    N -= 1
                  if NLed +1 == iterStep - offset:
                    for i in range(3):
                      printColor[i] = Effect['Color'][i]
                  else:
                    for i in range(3):
                      printColor[i] = LastColor[i]
              else:
                sys.exit('The effect type "' + Effect['Type'] + '" is unknown')
            else:
              for i in range(3):
                printColor[i] = LastColor[i]
            

            for i in range(3):
              writeVal(f,printColor[i],Ops,shouldBreak and i == 2)          
            if nbIter * Ops['Delay'] >= Ops['TimeLength']:
              break
            nbIter += 1

          if nbIter * Ops['Delay'] >= Ops['TimeLength']:
            break
        # Fill to have the same number of step
        if nbIter * Ops['Delay'] < Ops['TimeLength']:
          nbStep = int(Ops['TimeLength'] / Ops['Delay']) - nbIter -1
          for step in range(nbStep+1):
            for i in range(3):
              writeVal(f,LastColor[i],Ops, step == nbStep and i == 2)
        writeLedEnd(f,Ops,Led == N-1)
      writeSegEnd(f,Ops,idxSeg == nbSeg -1)

# Cannot open file
except IOError:
  sys.exit('Le fichier "' + Ops['Output'] + "\" n'a pas pu être ouvert")
