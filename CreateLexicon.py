import sys

# 输入的分好词的文件 RenMinData.txt
rawDataFile = "./RenMinData.txt"
# 输出 将token转变为id RenMinData.id.txt
idDataFile = "./RenMinData.id.txt"
# 输出 将token 对应的id 存入到文件 WordDic.rm.txt
wordDicFile = "./WordDic.rm.txt"

WordIDTable = {}

# 产生WordIDTable
id = 1
infile = open(rawDataFile, 'r', encoding='gb2312')
s = infile.readline().strip()
while len(s) > 0:
    #s = s.decode("gb2312")
    for word in s.split(' '):
        if word not in WordIDTable:
            WordIDTable[word] = id
            id += 1
    s = infile.readline().strip()
infile.close()
print("Reading raw data file finished!")
print("Total number of words:", len(WordIDTable))

# 将RenMinData.txt 转换成id，写入到 RenMinData.id.txt
infile = open(rawDataFile, 'r', encoding='gb2312')
outfile = open(idDataFile, 'w')
s = infile.readline().strip()
while len(s) > 0:
    #s = s.decode("gb2312")
    words = s.split(' ')
    for i in range(len(words)-1):
        word = words[i]
        if word not in WordIDTable:
            print("OOV word found!")
        else:
            outfile.write(str(WordIDTable[word]))
            outfile.write(' ')
    # 由于最后一个词后边不用再加空格，所以，这里单独写出
    word = words[len(words)-1]
    if word not in WordIDTable:  # 未登录词
        print("OOV word found!")
    else:
        outfile.write(str(WordIDTable[word]))
    outfile.write("\r\n")
    # 读下一行
    s = infile.readline().strip()
infile.close()
outfile.close()
print("Writing id data file finished!")

# 将WordIDTable 写入到文件 wordDicFile中
outfile = open(wordDicFile, 'w', encoding='gb2312')
for word in WordIDTable.keys():
    # outfile.write(word.encode("gb2312"))
    outfile.write(word)
    outfile.write(' ')
    outfile.write(str(WordIDTable[word]))
    outfile.write("\r\n")
outfile.close()
print("Writing word id table file finished!")
