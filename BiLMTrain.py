import sys

idDataFile = "./data/RenMinData.id.txt"
wordDicFile = "./data/WordDic.rm.txt"
biModelFile = "./data/BiModel.rm.txt"

WordIDTable = {}
BigramTableList = []  # 一元概率模型
UnigramCountList = []  # 二元概率模型
SmoothedProbList = []
TotalNum = 0

# load wordDicFile to WordIDTable
infile = open(wordDicFile, 'r', encoding='gb2312')
s = infile.readline().strip()
while len(s) > 0:
    #s = s.decode("gb2312")
    words = s.split(' ')
    if words[0] not in WordIDTable:
        WordIDTable[words[0]] = int(words[1])
    s = infile.readline().strip()
infile.close()
print("Reading word dic file finished!")
print("Total number of words:",len(WordIDTable))

# 初始化 BigramTableList UnigramCountList SmoothedProbList
lenWordIDTable = len(WordIDTable)
BigramTableList = [{} for _ in range(lenWordIDTable + 1)]  # why +1 ?
UnigramCountList = [0 for _ in range(lenWordIDTable + 1)]  # why +1 ?
SmoothedProbList = [0 for _ in range(lenWordIDTable + 1)]  # why +1 ?
# for i in range(len(WordIDTable)+1):
#     BigramTableList.append({})
#     UnigramCountList.append(0)
#     SmoothedProbList.append(0)

# 统计词频
infile = open(idDataFile, 'r')
s = infile.readline().strip()
while len(s) > 0:
    words = s.split(' ')
    widlist = []
    TotalNum += len(words)
    for word in words:
        widlist.append(int(word))
    for wordid in widlist:
        UnigramCountList[wordid] += 1
    for i in range(len(widlist)-1):
        tmpHT = BigramTableList[widlist[i]]
        if widlist[i+1] not in tmpHT:
            tmpHT[widlist[i+1]] = 1
        else:
            tmpHT[widlist[i+1]] += 1
    s = infile.readline().strip()
infile.close()
print("Reading id data file finished!")

#compute probabilities
for wid1 in range(1,len(WordIDTable)+1):
    SmoothedProbList[wid1] = 1/(float)(UnigramCountList[wid1] + len(WordIDTable))
    ht = BigramTableList[wid1]
    for wid2 in ht.keys():
        ht[wid2] = (float)(ht[wid2]+1) /(float)(UnigramCountList[wid1] + len(WordIDTable))
    UnigramCountList[wid1] = (float)(UnigramCountList[wid1])/(float)(TotalNum)

#save to file
outfile = open(biModelFile, 'w')
outfile.write(str(len(WordIDTable))+" "+str(TotalNum)+"\r\n")
for wid1 in range(1,len(WordIDTable)+1):
    outfile.write(str(UnigramCountList[wid1])+" ")
    outfile.write(str(SmoothedProbList[wid1]))
    ht = BigramTableList[wid1]
    for wid2 in ht.keys():
        outfile.write(" "+str(wid2)+" "+str(ht[wid2]))
    outfile.write("\r\n")
outfile.close()
print("Writing model file finished!")
