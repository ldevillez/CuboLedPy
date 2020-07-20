import json
import codecs
import sys

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

# Check if the data are good
nbSeg = len(data['Segments']) 
if nbSeg != 12:
    sys.exit('A cube has 12 edges. Your data has ' + str(nbSeg) +' edges')

#Options required
opsToTry = [
    'LedsBySegment',
    'TimeLength',
    'Delay',
    'Output',
    'Separator'
]

Ops = data['Options']

for op in opsToTry:
    if op not in Ops:
        sys.exit('The options must have a key "' + op + '"')

try:
    with open(Ops['Output'],'w+') as f:
        print('Ok ! Starting to work')
        for Seg in data['Segments']:
            for Led in range(Ops['LedsBySegment']):
                LastColor = [0, 0, 0]
                nbIter = 0
                for dataStep in Seg:
                    Li = [0, 0, 0]
                    Le = [0, 0, 0]

                    # SPATIAL
                    if dataStep['TypeSpatial'] == 'Linear':
                        for i in range(3):
                            #TODO handle Single led | LedsbySegment = 1
                            Li[i] = dataStep['ColorTiSi'][i] + (dataStep['ColorTiSe'][i] - dataStep['ColorTiSi'][i]) * Led / (Ops['LedsBySegment']-1)
                            Le[i] = dataStep['ColorTeSi'][i] + (dataStep['ColorTeSe'][i] - dataStep['ColorTeSi'][i]) * Led / (Ops['LedsBySegment']-1)
                    else:
                        print('bruuuuh')

                    # TEMPORAL
                    nbStep = int(dataStep['TimeLength'] / Ops['Delay'])
                    for step in range(nbStep):
                        shouldBreak = False
                        if (nbIter+1) * Ops['Delay'] >= Ops['TimeLength'] * 1000:
                            shouldBreak = True


                        if dataStep['TypeTemporal'] == 'Linear':
                            # TODO handle single step
                            for i in range(3):
                                LastColor[i] = int(Li[i] + (Le[i] - Li[i]) * step / (nbStep-1))
                                if shouldBreak and i == 2:
                                    f.write(
                                        str(int(Li[i] + (Le[i] - Li[i]) * step / (nbStep-1))) + "\n"
                                    )
                                else:
                                    f.write(
                                        str(int(Li[i] + (Le[i] - Li[i]) * step / (nbStep-1))) + Ops['Separator']
                                    )
                        
                        if nbIter * Ops['Delay'] >= Ops['TimeLength'] * 1000:
                            break
                        nbIter += 1

                    if nbIter * Ops['Delay'] >= Ops['TimeLength'] * 1000:
                        print('shoo')
                        break
                if nbIter * Ops['Delay'] < Ops['TimeLength'] * 1000:
                    nbStep = int(Ops['TimeLength'] * 1000 / Ops['Delay']) - nbIter -1
                    for step in range(nbStep):
                        for i in range(3):
                            f.write(str(LastColor[i]) + Ops['Separator'])
                    f.write(str(LastColor[0]) + Ops['Separator'] + str(LastColor[1]) + Ops['Separator'] + str(LastColor[2]) + "\n")

                    


            




# Cannot open file
except IOError:
    sys.exit('Le fichier "' + Ops['Output'] + "\" n'a pas pu être ouvert")
