sStr1 = 'ab,cde,fgh,ijk'
sStr2 = ','
sStr4 = sStr1[sStr1.find(sStr2) + 1:]
sStr3 = sStr1[:sStr1.find(sStr2)]
print(sStr3)
print(sStr4)
