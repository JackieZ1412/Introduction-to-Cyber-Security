import codecs
import os

path = '/home/zya1412/PAC-Proj1-master/PAC-Proj1-master/NodeLists'
for filename in os.listdir(path):
    print(filename)
    os.chdir(path)
    data = codecs.open(filename,'r','utf-8')
    line = data.readline()

    while line:
        print(line.encode('utf-8'))
        userID = line[:line.find(' ')].encode('utf-8')
        userName = line[line.find(' ')+1:].encode('utf-8')
        print("userID, userName ", userID, userName)
        line = data.readline()
    data.close()