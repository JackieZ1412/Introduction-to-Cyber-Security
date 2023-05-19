import codecs
import os

path = '/home/zya1412/PAC-Proj1-master/PAC-Proj1-master/NodeLists'
os.chdir(path)

data = codecs.open('nohuplog.txt','r','utf-8')
line=data.readline()
pointer = "START"
#print "line: ", line
dat=codecs.open('readlineFiles.txt','w+','utf-8')
while line:
    #print "what the hell \n", line
    if line.strip():
        if line != pointer:
            userID = line[line.find(':  ')+3:]
            dat.write("%s" %userID)

    pointer = line #put here because duplicate one alawys after the blank line
    line=data.readline()
dat.close()
data.close()

#### The code for extract the crawling sequence file in nodes
filePath ='/home/zya1412/PAC-Proj1-master/PAC-Proj1-master/Nodes'
seedNodes=codecs.open('readlineFiles.txt','r','utf-8')
os.chdir(filePath)
sequencialNodes = codecs.open('seqNodes.txt','w+','utf-8')
line = seedNodes.readline()
file_Numbers=0
while line:
    if file_Numbers>=1289: break
    #print "line", line
    #if file_Numbers==1289: ##Really Weird
        #line="20642645"
        #print "1290 line:",line
    line=line.strip()

    findFile = codecs.open(line+'.txt','r','utf-8')

    fileContent=findFile.read()
    sequencialNodes.write("%s" %fileContent)
    findFile.close
    file_Numbers=file_Numbers+1
    line=seedNodes.readline()

sequencialNodes.close
seedNodes.close
print ("the number of files:",file_Numbers)
