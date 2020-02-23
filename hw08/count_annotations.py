from xml.etree import ElementTree as ET
import os
cwd = os.getcwd()
count_file = 0
count_tie = 0
count_falcon = 0
for f in os.listdir(cwd + "/annotations/"):
    count_file += 1
    tree = ET.parse(cwd + "/annotations/" + f)
    for e in tree.findall('//name'):
        if e.text == 'Tie Fighter':
            count_tie += 1
        if e.text == 'the Millennium Falcon':
            count_falcon += 1
print(count_file)
print(count_tie)
print(count_falcon)
