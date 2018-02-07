#encoding:utf-8  


f = open("C:\Users\Frank\Desktop\\time.csv")
lines =f.readlines()
i=0
data = {}


for line in lines:
    transcations = [[0]*30]
    line=line.strip('\n')
    user=line.split(",")
    # print user[0]
    # print user[1]
    if user[1].strip()=='':
        user[1]=0
    if int(user[1])>30:
        user[1]=0
    # print user[1]
    # print int(user[1])-1
    if data.has_key(user[0]):
        if int(user[1])>0:
            data[user[0]][0][int(user[1])-1]=1
    else:
        data[user[0]]=transcations
        if int(user[1])>0:
            data[user[0]][0][int(user[1])-1]=1

        i+=1

for key in sorted(data.keys()):
    print key,
    # print '--->',
    # print list(data[key])
    # if len(data[key])>1:
    print data[key]


    #data_set.append(list(data[key]))
#print data_set


f.close()