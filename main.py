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

