import numpy as np
from collections import Counter

lines =[line.strip() for line in open('wsj00-18.tag','r') if '' in line ]
lines = ['</s>\t</s>' if x=='' else x for x in lines]
lines.insert(0,'<s>\t<s>')
for x in range(0,lines.count('</s>\t</s>') + len(lines) - 2):
    if(lines[x] == '</s>\t</s>'):
        lines.insert(x+1,'<s>\t<s>')
        
wordtags = [(l.split("\t")[0],l.split("\t")[1]) for l in lines]
wordset = [x for x,y in wordtags]
tagset = [y for x,y in wordtags]
tagbiagram = [(tagset[x-1],tagset[x]) for x in range(1,len(tagset))]
c = Counter(y for x,y in wordtags)
c1 = Counter((x,y) for x,y in wordtags)
c2 = Counter((x,y) for x,y in tagbiagram)
n=len(set(wordset))
m=len(set(tagset))
nword=list(set(wordset))
mtag=list(set(tagset))
mtag.remove('<s>')
mtag.remove('</s>')
mtag.insert(0,'<s>')
mtag.append('</s>')

emitcounts= {(nword[k],mtag[v]):(c1.get((nword[k],mtag[v]))/c.get(mtag[v]) if(c1.get((nword[k],mtag[v]))) else 0) for k in range(0, n) for v in range(0,m)} 
emitcounts['</s>','<s>']=0
transmitcounts = {(mtag[i],mtag[j]):(c2.get((mtag[i],mtag[j]))/c.get(mtag[i]) if(c2.get((mtag[i],mtag[j]))) else 0) for i in range(0,m) for j in range(0,m)}
transmitcounts['</s>','<s>']=0

print(c.get(('VBP')))
print(c2.get(('NNP','NNP')))
print(transmitcounts.get(('VBP','NNP')))

def viterbi(string1):
    l =[]
    string1.insert(0,'<s>')
    string1.append('</s>')
    V = np.zeros((len(mtag),len(string1)))  #47,7
    V[0,0] = 1
    s1 = 0
    bp = np.zeros((len(mtag),len(string1)),dtype=np.int)
    for s in range(1,46):
        V[s,1] = transmitcounts.get(('<s>',mtag[s])) * emitcounts.get((string1[1],mtag[s]))
        bp[s,1] = 0
    for t in range(2,len(string1)-1):
        for s in range(1,46):
            max = 0
            for k in range(1,46):
               temp = V[k,t-1] * transmitcounts.get((mtag[k],mtag[s]))
               if(max < temp):
                   max = temp
                   s1 = k
            V[s,t] = max  * emitcounts.get((string1[t],mtag[s]))
            bp[s,t] = s1
    max = 0
    for s in range(1,46):
        temp= V[s,len(string1)-2] * transmitcounts.get((mtag[s],'</s>')) 
        if(max <= temp):
                   max = temp
                   s1 = s
    V[len(mtag)-1,len(string1)-1] = max * emitcounts.get((string1[t],mtag[s]))   
    bp[len(mtag)-1,len(string1)-1] = s1
    x = bp[-1,-1]
    l.append(mtag[x])
    for i in range(len(string1)-2,1,-1):
        x=bp[x,i]
        l.append(mtag[x])
    return l[::-1]

print(viterbi(['This','is','a','sentence','.']))
print(viterbi(['This','might','produce','a','result','if','the','system','works','well','.']))
print(viterbi(['Can','a','can','can','a','can','?']))
print(viterbi(['Can','a','can','move','a','can','?']))
print(viterbi(['Can','you','walk','the','walk','and','talk','the','talk','?']))



