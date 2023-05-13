import sys

WordDic = {}
MaxWordLen = 1
# 加载语料库，得到WordDic，MaxWordLen
def LoadLexicon(lexiconFile):
    global MaxWordLen
    infile = open(lexiconFile, 'r', encoding='gb2312')
    s = infile.readline().strip()
    while len(s) > 0:
        #s = s.decode("gb2312")
        WordDic[s] = 1
        if len(s) > MaxWordLen:
            MaxWordLen = len(s)
        s = infile.readline().strip()
    infile.close()

def BMM(s):
    global MaxWordLen
    wordlist = []
    i = len(s)
    while i > 0:
        start = i - MaxWordLen
        if start < 0:
            start = 0
        while start < i:
            tmpWord = s[start:i]
            if tmpWord in WordDic:
                wordlist.insert(0, tmpWord)
                break
            else:
                start += 1
        if start >= i:
            wordlist.insert(0, s[i-1:i])
            start = i - 1
        i = start
    return wordlist

def PrintSegResult(wordlist):
    print("After word-seg:")
    for i in range(len(wordlist)-1):
        print(wordlist[i])
    print(wordlist[len(wordlist)-1])

LoadLexicon("./lexicon.txt")

# inputStr = u"南京市长江大桥"
inputStr = u"北京大学生活动中心"

wordlist = BMM(inputStr)
PrintSegResult(wordlist)

