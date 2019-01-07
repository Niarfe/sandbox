# Import the os module, for the os.walk function
import os
import json

# Set the directory you want to start from
rootDir = '.'
for dirName, subdirList, fileList in os.walk(rootDir):
    #print('Found directory: %s' % dirName)
    for fname in fileList:
        # print('\t%s' % fname)
        if fname == 'hits.json':
            #print("we're getting content for ",fname)
            with open(dirName+'/'+fname, 'r') as source:
                objs = json.loads(source.read())
            #print(type(objs))
            for obj in objs:
                print(obj['content'])
