import json
import math
import os
import re
import sys

def fileFinder(base) :
    directories = [base]
    while len(directories) :
        nextdir = []
        for pdir in directories :
            for f in os.listdir(pdir) :
                curdir = None
                runningdir = os.path.join( pdir, f )
                if os.path.isdir( runningdir ) :
                    nextdir.append( runningdir )
                else :
                    yield runningdir
        directories = nextdir

def classifyFiles(root):
    f1 =  open('nbmodel.txt','r')
    model = f1.read()
    print(model)
    model = json.loads(model)
    print(model)
    output = []
    for f in fileFinder(root):
        print(f)
        file = open(f, 'r', encoding="latin1")
        # print(file.read())
        s = file.read()
        tokens = re.split(r'(\s|\n)', s)
        spamprob = 0
        hamprob = 0
        for token in tokens:
            #start with spam
            if token in model['p(token|spam)']:
                spamprob += math.log(model['p(token|spam)'][token],10)
            if token in model['p(token|ham)']:
                hamprob += math.log(model['p(token|ham)'][token],10)
        spamprob += math.log(model['pspam'])
        hamprob += math.log(model['pham'])
        #if spamprob > -0.301029995664:
        print(spamprob,hamprob)
        if spamprob < hamprob:
            output.append('spam '+f)
        else:
            output.append('ham ' +f)
        ostr = ''
    for i in output:
        ostr += i + '\n'
    f2 = open('nboutput.txt', 'w')
    f2.write(ostr)
    f2.close()

    print(output)

#classifyFiles(sys.argv[1])
classifyFiles('C:\\Users\\dell pc\\Documents\\BackupDocuments\\Courses\\NLP\\Assignment1\\dev')