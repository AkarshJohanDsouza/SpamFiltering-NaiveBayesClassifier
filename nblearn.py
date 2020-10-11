import os
import collections
import re
import json
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

#################################
hammp = collections.Counter()
spammp = collections.Counter()
hamspamdict = {}
hamspamdict['ham'] = hammp
hamspamdict['spam'] = spammp
cntdict = collections.Counter()
wordcnt = {}
#################################
wordcnt['ham'] = 0
wordcnt['spam'] = 0
#################################
pHamMap = {}
pSpamMap = {}
phamspammap = {}
phamspammap['ham'] = pHamMap
phamspammap['spam'] = pSpamMap
pham = 0
pspam = 0

def trainmodel(base) :
    fc = 0
    maxwrd = {}
    maxwrd['ham'] = 0
    maxwrd['spam'] = 0
    totalfiles = 0

    for f in fileFinder(base):
        #print(f)
        fc += 1
        flg = f.split('.')[-2]
        #print(flg)
        if flg not in ['spam', 'ham']:
            continue
        cntdict[flg] +=1
        #print(flg)
        file = open(f,'r', encoding="latin1")
        #print(file.read())
        s = file.read()
        tokens = re.split(r'(\s|\n)',s)
        for token in tokens:
            hamspamdict[flg][token] += 1
            if hamspamdict[flg][token] > maxwrd[flg]:
                maxwrd[flg] = hamspamdict[flg][token]
            wordcnt[flg] +=1
    # print(hamspamdict['ham'])
    # print(fc)
    # print(hamspamdict[flg][token])
    pham = cntdict['ham']/(cntdict['ham']+cntdict['spam'])
    #print('p(ham) =',pham)
    pspam = cntdict['spam'] / (cntdict['ham'] + cntdict['spam'])
    # print('p(sham) =', pspam)
    # print('max ham words: ', maxwrd['ham'])
    # print('max spam words: ', maxwrd['spam'])
    model = {}
    model['pham'] = pham
    model['pspam'] = pspam
    ####################
    sumpham = 0
    sumpspam = 0
    hamspamsum = {}
    hamspamsum['ham'] = 0
    hamspamsum['spam'] = 0
    v = len(hamspamdict['ham'].keys()) + len(hamspamdict['spam'].keys())
    for c in hamspamdict:
        for token in hamspamdict[c]:
            phamspammap[c][token] = (hamspamdict[c][token] + 1) / (wordcnt[c] + v)
            hamspamsum[c] += phamspammap[c][token]
    for c in hamspamdict: #normalize pham and pspam
        for token in hamspamdict[c]:
            phamspammap[c][token] = (phamspammap[c][token] + 1) / (hamspamsum[c] + v)

    #print(phamspammap)
    model['p(token|ham)'] = phamspammap['ham']
    model['p(token|spam)'] = phamspammap['spam']
    #print('model',model)
    f1 = open('nbmodel.txt', 'w')
    f1.write(json.dumps(model))
    f1.close()

#trainmodel(sys.argv[1])
trainmodel("C:\\Users\\dell pc\\Documents\\BackupDocuments\\Courses\\NLP\\Assignment1\\train10")